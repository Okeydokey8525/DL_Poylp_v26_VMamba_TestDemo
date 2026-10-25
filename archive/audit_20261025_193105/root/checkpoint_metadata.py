"""Compare embedded checkpoint provenance with the neighboring raw run, read-only."""
from pathlib import Path
import csv, gc, json, sys
import checkpoint_audit as audit

sys.stdout.reconfigure(encoding='utf-8')
records=[]
for model,seed,run in audit.runs():
    p=run/'weights/best.pt';rec={'model':model,'seed':seed,'path':str(p)}
    try:
        ck=audit.torch.load(p,map_location='cpu',weights_only=False)
        args=ck.get('train_args') or {};tr=ck.get('train_results')
        rec.update(checkpoint_seed=args.get('seed'),checkpoint_run_name=args.get('name'),
                   checkpoint_version=ck.get('version'),checkpoint_date=ck.get('date'),
                   stored_best_fitness=ck.get('best_fitness'),stored_train_metrics=ck.get('train_metrics'),
                   metadata_keys=list(ck),seed_matches=args.get('seed')==seed,
                   run_name_matches=args.get('name')==run.name,
                   embedded_results_type=type(tr).__name__)
        if isinstance(tr,dict):
            rec['embedded_results_columns']=list(tr)
            arrays={k.strip():v for k,v in tr.items() if isinstance(v,list)}
            with (run/'results.csv').open(encoding='utf-8-sig') as f:raw=[{k.strip():float(v) for k,v in r.items()} for r in csv.DictReader(f)]
            rec['embedded_results_lengths']={k:len(v) for k,v in arrays.items()}
            mismatches=[];checks=0
            for key,values in arrays.items():
                if key not in raw[0]:continue
                for i,v in enumerate(values):
                    if i>=len(raw):break
                    if isinstance(v,(int,float)):
                        checks+=1
                        if abs(v-raw[i][key])>1e-8*max(1,abs(v)):
                            mismatches.append({'epoch':i+1,'column':key,'embedded':v,'csv':raw[i][key]})
            rec['embedded_numeric_checks']=checks;rec['embedded_numeric_mismatch_count']=len(mismatches);rec['embedded_numeric_mismatch_examples']=mismatches[:6]
            if arrays.get('epoch'):rec['embedded_last_epoch']=arrays['epoch'][-1]
        del ck;gc.collect()
    except Exception as e:rec['error']=repr(e)
    records.append(rec)
    (audit.HERE/'checkpoint_metadata.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print(model,seed,'seed',rec.get('seed_matches'),'name',rec.get('run_name_matches'),'embedded_mismatches',rec.get('embedded_numeric_mismatch_count'),'last_epoch',rec.get('embedded_last_epoch'),flush=True)
print('COMPLETE',len(records),flush=True)
