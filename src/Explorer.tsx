import {useMemo,useState} from "react";
import {Search,ArrowLeft,Network} from "lucide-react";
import {stages} from "./data";
import {mathTopics} from "./mathTopics";
import {KnowledgeGraph,GraphNode} from "./KnowledgeGraph";
import "./explorer.css";
const names=["АНАЛИЗ","АЛГЕБРА","ГЕОМЕТРИЯ","ДОПОЛНИТЕЛЬНО"];
const sections:GraphNode[]=stages.flatMap((s,stage)=>s.tracks.map((title,lane)=>({id:stage+"-"+lane,title,stage,lane,requires:stage===0?[]:[(stage-1)+"-"+lane]})));
const total=Object.values(mathTopics).reduce((n,v)=>n+v.length,0);
export function Explorer(){
 const[section,setSection]=useState<string|null>(null);
 const[active,setActive]=useState("2-0");
 const[query,setQuery]=useState("");
 const[lane,setLane]=useState<number|null>(null);
 const base=sections.find(n=>n.id===section);
 const topics=useMemo<GraphNode[]>(()=>section?(mathTopics[section]||[]).map((title,i)=>({id:section+":"+i,title,stage:i,lane:0,requires:i? [section+":"+(i-1)]:[]})):sections,[section]);
 const selected=topics.find(n=>n.id===active)||topics[0];
 const shown=topics.filter(n=>(section!==null||lane===null||n.lane===lane)&&n.title.toLowerCase().includes(query.toLowerCase()));
 const chooseSection=(id:string)=>{setSection(id);setActive(id+":0");setQuery("")};
 const goBack=()=>{setSection(null);setActive(section||"2-0");setQuery("")};
 return <section className="explorer" aria-labelledby="explorer-title">
 <div className="explorer-heading"><div><div className="eyebrow">МАТЕМАТИКА / {sections.length} РАЗДЕЛОВ / {total} ПОДРАЗДЕЛОВ</div><h2 id="explorer-title">{base?base.title:"Граф математики"}<span className="period">.</span></h2><p>{base?"Вложенный граф подразделов выбранного направления.":"Выберите раздел графа, чтобы открыть его подробную структуру."}</p></div></div>
 {base&&<button className="graph-back" onClick={goBack}><ArrowLeft size={16}/> Общая карта математики</button>}
 <div className="explorer-controls"><div className="explorer-search"><Search size={16}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Найти тему..." aria-label="Найти тему"/></div></div>
 {!section&&<div className="explorer-filters"><button className={lane===null?"selected":""} onClick={()=>setLane(null)}>Все ветви</button>{names.map((n,i)=><button className={lane===i?"selected":""} key={n} onClick={()=>setLane(i)}>{n}</button>)}</div>}
 <div className="explorer-layout"><div className="explorer-canvas as-map"><KnowledgeGraph key={section||"overview"} nodes={shown} active={selected.id} onSelect={setActive}/></div>
 <aside className="explorer-detail"><div className="eyebrow">{section?"ПОДРАЗДЕЛ":"РАЗДЕЛ"}</div><span className="detail-number">{section?String(selected.stage+1).padStart(2,"0"):String(selected.stage+1).padStart(2,"0")+" / "+String.fromCharCode(65+selected.lane)}</span><h3>{selected.title}</h3>
 {!section?<><p className="detail-caption">{names[selected.lane]} · ЭТАП {selected.stage+1}</p><button className="detail-action" onClick={()=>chooseSection(selected.id)}><Network size={16}/> Открыть граф подразделов ({mathTopics[selected.id]?.length||0})</button><div className="detail-section"><h4>Подразделы</h4><div className="subtopic-list">{(mathTopics[selected.id]||[]).map((name,i)=><button className="subtopic-item subtopic-button" key={name} onClick={()=>{chooseSection(selected.id);setActive(selected.id+":"+i)}}><span>{String(i+1).padStart(2,"0")}</span>{name}</button>)}</div></div></>:<div className="detail-section"><h4>Раздел</h4><p>{base?.title}</p><h4>Соседние темы</h4>{topics.filter(n=>Math.abs(n.stage-selected.stage)===1).map(n=><button className="prereq" key={n.id} onClick={()=>setActive(n.id)}>→ {n.title}</button>)}</div>}
 {!section&&<><div className="detail-section"><h4>Предшествующие разделы</h4>{selected.requires.map(id=>{const n=sections.find(x=>x.id===id)!;return <button className="prereq" key={id} onClick={()=>{setActive(id);setLane(null);setQuery("")}}>↳ {n.title}</button>})}</div><div className="detail-section"><h4>Следующие разделы</h4>{sections.filter(n=>n.requires.includes(selected.id)).map(n=><button className="prereq" key={n.id} onClick={()=>{setActive(n.id);setLane(null);setQuery("")}}>→ {n.title}</button>)}</div></>}
 </aside></div><p className="explorer-note">Обзорная иерархия математики. Линии отражают навигационный порядок, а не полный перечень математических предпосылок.</p></section>
}