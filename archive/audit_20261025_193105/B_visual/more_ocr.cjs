const fs=require('fs');const path=require('path');
const {createWorker,PSM}=require('C:/Users/leduc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/tesseract.js');
(async()=>{
const base=__dirname;const jobs=JSON.parse(fs.readFileSync(path.join(base,'more_ocr_jobs.json'),'utf8'));
const worker=await createWorker('eng',1,{cachePath:path.join(base,'ocr_cache')});
const results=[];
for(let i=0;i<jobs.length;i++){
 const job=jobs[i];await worker.setParameters({tessedit_pageseg_mode:job.type==='full'||job.type==='legend'?PSM.AUTO:PSM.SINGLE_LINE});
 const {data}=await worker.recognize(job.path);
 results.push({...job,text:data.text,confidence:data.confidence});
 fs.writeFileSync(path.join(base,'more_ocr_results.json'),JSON.stringify(results,null,2));
 if(i%50===0)process.stdout.write(`${i+1}/${jobs.length}\n`);
}
await worker.terminate();console.log('OCR complete',results.length);
})().catch(e=>{console.error(e);process.exit(1)});

