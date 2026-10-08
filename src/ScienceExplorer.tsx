import {expandedSciences} from "./expandedSciences";
import {getSubtopics} from "./subtopics";
import {useMemo,useState} from "react";
import {Search,ArrowLeft,Network} from "lucide-react";
import {sciences} from "./data";
import {KnowledgeGraph,GraphNode} from "./KnowledgeGraph";
import "./explorer.css";
const branches:Record<string,string[][]>={
physics:[["Классическая механика","Аналитическая механика","Нелинейная динамика","Теория хаоса"],["Термодинамика","Статистическая физика","Фазовые переходы","Неравновесные системы"],["Электромагнетизм","Электродинамика","Квантовая электродинамика","Квантовая теория поля"],["Специальная относительность","Общая относительность","Космология","Квантовая гравитация"]],
cs:[["Дискретные структуры","Алгоритмы","Структуры данных","Теория сложности"],["Логические схемы","Архитектура ЭВМ","Операционные системы","Распределённые системы"],["Программирование","Языки и компиляторы","Формальные методы","Верификация"],["Вероятность и статистика","Машинное обучение","Глубокое обучение","Искусственный интеллект"]],
epistemology:[["Понятие знания","Обоснование","Проблема Геттиера","Современная эпистемология"],["Истина","Теории истины","Реализм и антиреализм","Социальная эпистемология"],["Скептицизм","Проблема индукции","Байесовская эпистемология","Формальная эпистемология"],["Восприятие","Свидетельство","Научное объяснение","Философия науки"]],
biology:[["Клеточная биология","Молекулярная биология","Генетика","Геномика"],["Анатомия","Физиология","Нейробиология","Системная биология"],["Эволюция","Популяционная генетика","Филогенетика","Эволюционная биология"],["Экология","Экосистемы","Биогеография","Биосфера"]],
chemistry:[["Строение атома","Химическая связь","Неорганическая химия","Координационная химия"],["Органическая химия","Механизмы реакций","Синтез","Химия полимеров"],["Термохимия","Физическая химия","Кинетика","Квантовая химия"],["Аналитическая химия","Спектроскопия","Электрохимия","Материаловедение"]],
philosophy:[["История философии","Онтология","Метафизика","Философия времени"],["Логика","Эпистемология","Философия науки","Философия математики"],["Этика","Метаэтика","Политическая философия","Прикладная этика"],["Философия языка","Философия сознания","Феноменология","Философия ИИ"]]
};
function topics(id:string){const detailed=expandedSciences[id];if(detailed)return detailed.map(n=>({id:n.id,title:n.title,stage:n.stage,lane:n.lane,requires:n.stage?[(n.stage-1)+"-"+n.lane]:[]}));const branch=branches[id]||[];return branch.flatMap((titles,lane)=>titles.map((title,stage):GraphNode=>({id:stage+"-"+lane,title,stage,lane,requires:stage?[(stage-1)+"-"+lane]:[]})))}
export function ScienceExplorer({scienceId}:{scienceId:string}){
 const science=sciences.find(s=>s.id===scienceId)!;
 const nodes=useMemo(()=>topics(scienceId),[scienceId]);
 const detailed=expandedSciences[scienceId];
 const[section,setSection]=useState<string|null>(null);
 const[active,setActive]=useState("0-0");
 const[query,setQuery]=useState("");
 const base=detailed?.find(n=>n.id===section);
 const graphNodes=useMemo<GraphNode[]>(()=>base?base.topics.map((title,i)=>({id:base.id+":"+i,title,stage:i,lane:0,requires:i?[base.id+":"+(i-1)]:[]})):nodes,[base,nodes]);
 const selected=graphNodes.find(n=>n.id===active)||graphNodes[0];
 const visible=graphNodes.filter(n=>n.title.toLowerCase().includes(query.toLowerCase()));
 const next=graphNodes.filter(n=>n.requires.includes(selected.id));
 const selectedDetails=detailed?.find(n=>n.id===selected.id);
 const open=(id:string,index=0)=>{setSection(id);setActive(id+":"+index);setQuery("")};
 return <section className="explorer">
 <div className="explorer-heading"><div><div className="eyebrow">{science.en} / {detailed?detailed.length+" РАЗДЕЛОВ / "+detailed.reduce((sum,n)=>sum+n.topics.length,0)+" ТЕМ":"ИНТЕРАКТИВНАЯ КАРТА"}</div><h2>{base?base.title:science.name}<span className="period">.</span></h2><p>{base?"Подробный граф выбранного раздела.":science.description}</p></div></div>
 {base&&<button className="graph-back" onClick={()=>{setSection(null);setActive(base.id);setQuery("")}}><ArrowLeft size={16}/> Общая карта {science.name.toLowerCase()}</button>}
 <div className="explorer-controls"><div className="explorer-search"><Search size={16}/><input aria-label="Поиск раздела" placeholder="Найти тему..." value={query} onChange={e=>setQuery(e.target.value)}/></div></div>
 <div className="explorer-layout"><div className="explorer-canvas as-map"><KnowledgeGraph key={section||scienceId} nodes={visible} active={selected.id} onSelect={setActive}/></div><aside className="explorer-detail"><div className="eyebrow">{base?"ТЕМА":"РАЗДЕЛ"}</div><span className="detail-number">{String(selected.stage+1).padStart(2,"0")}</span><h3>{selected.title}</h3>
 {!base&&detailed&&selectedDetails&&<><button className="detail-action" onClick={()=>open(selected.id)}><Network size={16}/> Открыть граф подразделов ({selectedDetails.topics.length})</button><div className="detail-section"><h4>Подразделы</h4><div className="subtopic-list">{selectedDetails.topics.map((name,i)=><button className="subtopic-item subtopic-button" key={i} onClick={()=>open(selected.id,i)}><span>{String(i+1).padStart(2,"0")}</span>{name}</button>)}</div></div></>}
 {!base&&!detailed&&<div className="detail-section"><h4>Подразделы</h4><div className="subtopic-list">{getSubtopics(selected.title).map((name,i)=><div className="subtopic-item" key={i}><span>{String(i+1).padStart(2,"0")}</span>{name}</div>)}</div></div>}
 <div className="detail-section"><h4>{base?"Соседние темы":"Предшествующие связи"}</h4>{selected.requires.map(id=>{const n=graphNodes.find(n=>n.id===id);return n&&<button className="prereq" key={id} onClick={()=>setActive(id)}>↳ {n.title}</button>})}</div>
 <div className="detail-section"><h4>Следующие темы</h4>{next.map(n=><button className="prereq" key={n.id} onClick={()=>setActive(n.id)}>→ {n.title}</button>)}</div></aside></div><p className="explorer-note">Исторические направления могут сосуществовать и влиять друг на друга; линии отражают порядок обзора, а не единую хронологию или строгое происхождение идей.</p></section>
}
