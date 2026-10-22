// Rebuild the Excel report from the canonical CSV. Run from any working folder.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const policy = JSON.parse(await fs.readFile(path.join(root, 'tracking/study-targets.json'), 'utf8'));
const modules = process.env.CODEX_NODE_MODULES || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const requireRuntime = createRequire(path.join(modules, '../package.json'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(requireRuntime.resolve('@oai/artifact-tool')).href);
const out = path.join(root, 'outputs/study-tracker');
await fs.mkdir(out, { recursive: true });
const csv = await fs.readFile(path.join(root, 'tracking/study-log.csv'), 'utf8');
const wb = await Workbook.fromCSV(csv, { sheetName: 'Sessions' });
const source = wb.worksheets.getItem('Sessions');
// Add outputs first in a fresh workbook, keeping imported CSV values intact.
const book = Workbook.create();
const daily = book.worksheets.add('Daily');
const weekly = book.worksheets.add('Weekly');
const sessions = book.worksheets.add('Sessions');
// Preserve ISO timestamps as text; CSV auto-detection can otherwise convert them.
function parseCsv(text) {
 const rows=[]; let row=[],field='',quoted=false;
 for(let i=0;i<text.length;i++) {
  const c=text[i];
  if(c==='"') { if(quoted && text[i+1]==='"') {field+='"';i++;} else quoted=!quoted; }
  else if(c===',' && !quoted) {row.push(field);field='';}
  else if((c==='\n'||c==='\r') && !quoted) {if(c==='\r'&&text[i+1]==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field='';}
  else field+=c;
 }
 if(field||row.length){row.push(field);rows.push(row);}
 return rows;
}
const raw = parseCsv(csv.replace(/^\uFEFF/,''));
const serial = s => (Date.parse(s.slice(0,10) + 'T00:00:00Z') - Date.UTC(1899,11,30)) / 86400000;
const iso = n => new Date(Date.UTC(1899,11,30) + n * 86400000).toISOString().slice(0,10);
const today = process.argv[2] || new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
if (!/^\d{4}-\d{2}-\d{2}$/.test(today)) throw Error('Use YYYY-MM-DD as reporting date.');
const first = serial(policy.tracking_start), deadline = serial(policy.preparation_deadline);
const last = Math.max(deadline, serial(today));
const ids = new Set();
for (const r of raw.slice(1)) {
  if (ids.has(r[0])) throw Error(`Duplicate session ID: ${r[0]}`);
  ids.add(r[0]);
  r[1] = serial(r[1]);
  if (r[6] === 'completed') {
    if (!r[3] || !r[4] || r[5] === '' || r[5] == null) throw Error(`Incomplete completed interval: ${r[0]}`);
    r[5] = Number(r[5]);
    if (!Number.isFinite(r[5]) || r[5] < 0 || Math.abs((Date.parse(r[4])-Date.parse(r[3]))/60000-r[5]) > 0.1) throw Error(`Invalid duration: ${r[0]}`);
  } else r[5] = r[5] === '' || r[5] == null ? null : Number(r[5]);
}
sessions.getRange(`A1:H${raw.length}`).values = raw.map((r,i)=>r.map((v,c)=>i>0 && (c===3||c===4) && v ? `IST ${String(v).replace('T',' ').replace('+05:30','')}` : v));
const sourceLast = Math.max(raw.length, 2);
const sumDay = r => `SUMIFS('Sessions'!$F$2:$F$${sourceLast},'Sessions'!$B$2:$B$${sourceLast},A${r},'Sessions'!$G$2:$G$${sourceLast},"completed")/60`;
daily.getRange('A2').values = [['Study hours: daily progress']];
daily.getRange('A4:B9').values = [['Reporting date (IST)',serial(today)],['Tracking starts',first],['Weekday target (from 22 Oct)',7],['Weekend target (hours)',10],['New target effective',serial(policy.preparation_start)],['Preparation deadline',deadline]];
daily.getRange('G4:H5').values = [['Earlier weekday target',6],['Target source','tracking/study-targets.json']];
// Derive both historical and current controls from the shared policy.
daily.getRange('H4').values = [[policy.targets[0].weekday_hours]];
daily.getRange('B6:B7').values = [[policy.targets.at(-1).weekday_hours],[policy.targets.at(-1).weekend_hours]];
daily.getRange('D4:E8').values = [['Confirmed hours',null],['Target: closed days',null],['Behind: closed days',null],['Ahead: closed days',null],['Remaining today',null]];
daily.getRange('A10').values = [['Hours are decimal: 1.50 = 1 hour 30 minutes. Zero means no confirmed time logged.']];
daily.getRange('A11').values = [['Uncertain and running intervals are excluded. Today is in progress; future days are not overdue.']];
daily.getRange('A12').values = [['Report refreshed from study-log.csv; rerun the builder after timer changes. Reporting date is fixed in IST.']];
daily.getRange('A14:J14').values = [['Date','Day','Week starting','Target (h)','Confirmed (h)','Behind (h)','Ahead (h)','Cumulative target','Cumulative actual','Record status']];
const n = last-first+1, end = 14+n;
const data = [];
const forms = [];
for (let i=0;i<n;i++) {
 const r=15+i,d=first+i;
 data.push([d,new Date(iso(d)+'T00:00:00Z').toLocaleDateString('en-US',{weekday:'short',timeZone:'UTC'})]);
 forms.push([`=A${r}-WEEKDAY(A${r},2)+1`,`=IF(WEEKDAY(A${r},2)>5,$B$7,IF(A${r}<$B$8,$H$4,$B$6))`,`=IF(A${r}>$B$4,"",${sumDay(r)})`,`=IF(A${r}>=$B$4,"",MAX(D${r}-E${r},0))`,`=IF(A${r}>=$B$4,"",MAX(E${r}-D${r},0))`,`=IF(A${r}>=$B$4,"",SUM($D$15:D${r}))`,`=IF(A${r}>$B$4,"",SUM($E$15:E${r}))`,`=IF(A${r}>$B$4,"Future",IF(A${r}=$B$4,"In progress",IF(COUNTIFS('Sessions'!$B$2:$B$${sourceLast},A${r},'Sessions'!$G$2:$G$${sourceLast},"needs_confirmation")>0,"Uncertain time",IF(E${r}=0,"No confirmed time","Logged"))))`]);
}
daily.getRange(`A15:B${end}`).values=data;
daily.getRange(`C15:J${end}`).formulas=forms;
daily.getRange('E4:E8').formulas=[
 [`=SUM(E15:E${end})`],
 [`=SUMIFS(D15:D${end},A15:A${end},"<"&B4)`],
 [`=MAX(E5-SUMIFS(E15:E${end},A15:A${end},"<"&B4),0)`],
 [`=MAX(SUMIFS(E15:E${end},A15:A${end},"<"&B4)-E5,0)`],
 [`=MAX(SUMIFS(D15:D${end},A15:A${end},B4)-SUMIFS(E15:E${end},A15:A${end},B4),0)`]
];
weekly.getRange('A2').values=[['Study hours: weekly progress']];
weekly.getRange('A4').values=[['Monday–Sunday: first partial 32 h; transition 52 h; full new weeks 55 h; final preparation partial 35 h.']];
weekly.getRange('A5').values=[['Behind compares confirmed time with targets for closed days only. Remaining includes today and future days.']];
weekly.getRange('A7:H7').values=[['Week starting','Weekly target (h)','Closed-day target','Confirmed (h)','Behind closed days','Ahead closed days','Remaining to target','Completion']];
const monday=first-((new Date(iso(first)+'T00:00:00Z').getUTCDay()+6)%7);
let wr=8;
for(let d=monday;d<=last;d+=7,wr++) {
 const cutoff = d<=deadline ? Math.min(d+6,deadline) : d+6;
 const clip = `,'Daily'!$A$15:$A$${end},"<=${cutoff}"`;
 weekly.getRange(`A${wr}`).values=[[d]];
 weekly.getRange(`B${wr}:H${wr}`).formulas=[[
 `=SUMIFS('Daily'!$D$15:$D$${end},'Daily'!$C$15:$C$${end},A${wr}${clip})`,
 `=SUMIFS('Daily'!$D$15:$D$${end},'Daily'!$C$15:$C$${end},A${wr},'Daily'!$A$15:$A$${end},"<"&'Daily'!$B$4${clip})`,
 `=SUMIFS('Daily'!$E$15:$E$${end},'Daily'!$C$15:$C$${end},A${wr}${clip})`,
 `=MAX(C${wr}-SUMIFS('Daily'!$E$15:$E$${end},'Daily'!$C$15:$C$${end},A${wr},'Daily'!$A$15:$A$${end},"<"&'Daily'!$B$4${clip}),0)`,
 `=MAX(SUMIFS('Daily'!$E$15:$E$${end},'Daily'!$C$15:$C$${end},A${wr},'Daily'!$A$15:$A$${end},"<"&'Daily'!$B$4${clip})-C${wr},0)`,
 `=MAX(B${wr}-D${wr},0)`,`=IF(B${wr}=0,0,D${wr}/B${wr})`]];
}
for(const sh of [daily,weekly,sessions]) {
 sh.showGridLines=false;
 sh.getUsedRange().format.font={name:'Arial',size:10,color:'#243247'};
 sh.getUsedRange().format.rowHeight=22;
 sh.getUsedRange().format.columnWidth=19;
}
for(const [sh,header] of [[daily,'A14:J14'],[weekly,'A7:H7'],[sessions,'A1:H1']]) {
 sh.getRange(header).format={fill:'#253C5B',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:34};
}
daily.getRange('A2').format.font={size:16,bold:true};
weekly.getRange('A2').format.font={size:16,bold:true};
daily.getRange(`D15:I${end}`).setNumberFormat('0.00');
daily.getRange('E4:E8').setNumberFormat('0.00');
daily.getRange('B4:B5').setNumberFormat('dd mmm yyyy');
daily.getRange('B8:B9').setNumberFormat('dd mmm yyyy');
daily.getRange('B4:B7').format.fill='#FFF2CC';
daily.getRange(`A15:A${end}`).setNumberFormat('dd mmm yyyy');
daily.getRange(`C15:C${end}`).setNumberFormat('dd mmm yyyy');
daily.getRange(`J15:J${end}`).format.columnWidth=24;
daily.getRange('A4:A7').format.columnWidth=25;
daily.getRange('D4:D8').format.columnWidth=23;
weekly.getRange(`A8:A${wr-1}`).setNumberFormat('dd mmm yyyy');
weekly.getRange(`B8:G${wr-1}`).setNumberFormat('0.00');
weekly.getRange(`H8:H${wr-1}`).setNumberFormat('0%');
sessions.getRange(`B2:B${sourceLast}`).setNumberFormat('dd mmm yyyy');
sessions.getRange('A1:A2').format.columnWidth=29;
sessions.getRange('C1:C2').format.columnWidth=33;
sessions.getRange('D1:E2').format.columnWidth=32;
sessions.getRange('G1:G2').format.columnWidth=25;
sessions.getRange('H1:H2').format.columnWidth=90;
daily.freezePanes.freezeRows(14); weekly.freezePanes.freezeRows(7); sessions.freezePanes.freezeRows(1);
for(const [sh,range] of [[daily,`F15:F${end}`],[weekly,`E8:E${wr-1}`]]) sh.getRange(range).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:0,format:{fill:'#FCE8E6',font:{color:'#9C2424'}}});
// Exercise a completed 90-minute interval and the next-day cutoff, then restore.
if(raw.length===2 && raw[1][6]==='needs_confirmation') {
 sessions.getRange('F2:G2').values=[[90,'completed']];
 daily.getRange('B4').values=[[first+1]];
 if(Number(daily.getRange('E15').values[0][0])!==1.5 || Number(daily.getRange('F15').values[0][0])!==4.5 || Number(daily.getRange('E6').values[0][0])!==4.5) throw Error('Completed interval or date cutoff mismatch');
 sessions.getRange('F2:G2').values=[[raw[1][5],raw[1][6]]];
 daily.getRange('B4').values=[[serial(today)]];
}
book.recalculate();
console.log((await book.inspect({kind:'region',sheetId:'Daily',range:'D4:E8',maxChars:1600,tableMaxRows:6})).ndjson);
console.log((await book.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:10},maxChars:1200})).ndjson);
// Validate representative boundaries against the imported source, then restore.
const baseline=daily.getRange('E15').values[0][0];
if (Number(baseline)!==0 && raw.length===2 && raw[1][6]==='needs_confirmation') throw Error('Unconfirmed time counted');
const expectedWeeks = {'2026-10-12':32, '2026-10-19':52, '2026-10-26':55, '2026-12-28':55};
expectedWeeks['2027-01-18'] = 35;
for (let r=8;r<wr;r++) {
 const start = iso(Number(weekly.getRange(`A${r}`).values[0][0]));
 if (start in expectedWeeks && Number(weekly.getRange(`B${r}`).values[0][0]) !== expectedWeeks[start]) throw Error(`Weekly target mismatch: ${start}`);
}
for (const [date, expected] of [['2026-10-21',6],['2026-10-22',7],['2026-10-24',10],['2027-01-22',7]]) {
 const row=15+serial(date)-first;
 if(Number(daily.getRange(`D${row}`).values[0][0])!==expected) throw Error(`Daily target mismatch: ${date}`);
}
// Topic summaries retain source labels, including mixed/setup topics; no retrospective classification.
const topics = book.worksheets.add('Topics');
topics.getRange('A2').values = [['Confirmed time by source topic']];
topics.getRange('A4').values = [['Exact source labels. Mixed/setup time does not prove technology proficiency.']];
topics.getRange('A6:B6').values = [['Source topic','Confirmed hours']];
const labels = [...new Set(raw.slice(1).map(r=>r[2]))].sort();
topics.getRange(`A7:A${6+labels.length}`).values=labels.map(v=>[v]);
topics.getRange(`B7:B${6+labels.length}`).formulas=labels.map((_,i)=>[`=SUMIFS('Sessions'!$F$2:$F$${sourceLast},'Sessions'!$C$2:$C$${sourceLast},A${i+7},'Sessions'!$G$2:$G$${sourceLast},"completed",'Sessions'!$B$2:$B$${sourceLast},"<="&'Daily'!$B$4)/60`]);
topics.showGridLines=false;
topics.getRange(`A6:B${6+labels.length}`).format.font={name:'Arial',size:10,color:'#243247'};
topics.getRange('A6:B6').format={fill:'#253C5B',font:{bold:true,color:'#FFFFFF'},rowHeight:28};
topics.getRange('A1:A2').format.columnWidth=65;
topics.getRange('B1:B2').format.columnWidth=20;
topics.getRange(`B7:B${6+labels.length}`).setNumberFormat('0.00');
book.recalculate();
const sourceHours=raw.slice(1).filter(r=>r[6]==='completed' && r[1]<=serial(today)).reduce((sum,r)=>sum+r[5]/60,0);
const reportedHours=Number(daily.getRange('E4').values[0][0]);
if(Math.abs(sourceHours-reportedHours)>0.000001) throw Error('Confirmed hours do not reconcile');
const topicHours=topics.getRange(`B7:B${6+labels.length}`).values.reduce((sum,r)=>sum+Number(r[0]),0);
if(Math.abs(sourceHours-topicHours)>0.000001) throw Error('Topic hours do not reconcile');
for(const sheet of [daily,weekly,sessions,topics]) {
 if(sheet.getUsedRange().values.flat().some(v=>typeof v==='string' && /^#(REF!|DIV\/0!|VALUE!|NAME\?|NUM!|SPILL!|N\/A)/.test(v))) throw Error(`Formula error in ${sheet.name}`);
}
const xlsx=await SpreadsheetFile.exportXlsx(book);
await xlsx.save(path.join(out,'study-hours.xlsx'));
for(const [sh,range] of [['Daily','A2:J23'],['Weekly','A2:H12'],['Sessions','A1:G2'],['Topics',`A2:B${6+labels.length}`]]) {
 const preview=await book.render({sheetName:sh,range,scale:1,format:'png'});
 await fs.writeFile(path.join(out,`${sh.toLowerCase()}-preview.png`),new Uint8Array(await preview.arrayBuffer()));
}
console.log(`Saved ${path.join(out,'study-hours.xlsx')} | reporting date ${today}`);
