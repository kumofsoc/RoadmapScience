import {useRef,useState} from "react";
import {Plus,Minus,Maximize2} from "lucide-react";
import "./graph.css";
export type GraphNode={id:string;title:string;stage:number;lane:number;requires:string[]};
const W=255,H=96,GX=305,GY=140,PAD=45;
export function KnowledgeGraph({nodes,active,onSelect}:{nodes:GraphNode[];active:string;onSelect:(id:string)=>void}){
 const [zoom,setZoom]=useState(.8),[offset,setOffset]=useState({x:0,y:0});
 const drag=useRef<{x:number;y:number;ox:number;oy:number;moving:boolean}|null>(null);
 const width=15*GX+PAD*2,height=4*GY+PAD*2;
 const pos=(n:GraphNode)=>({x:PAD+n.stage*GX,y:PAD+n.lane*GY});
 const ids=new Set(nodes.map(n=>n.id));
 const edges=nodes.flatMap(n=>n.requires.filter(id=>ids.has(id)).map(id=>({from:id,to:n.id})));
 const lookup=new Map(nodes.map(n=>[n.id,n]));
 const changeZoom=(factor:number)=>setZoom(v=>Math.max(.35,Math.min(1.7,Math.round(v*factor*100)/100)));
 return <div className="graph-shell">
 <div className="graph-toolbar"><span>ПЕРЕТАСКИВАЙ · МАСШТАБИРУЙ</span><div><button aria-label="Уменьшить масштаб" onClick={()=>changeZoom(.8)}><Minus size={16}/></button><span>{Math.round(zoom*100)}%</span><button aria-label="Увеличить масштаб" onClick={()=>changeZoom(1.25)}><Plus size={16}/></button><button aria-label="Сбросить вид" onClick={()=>{setZoom(.8);setOffset({x:0,y:0})}}><Maximize2 size={16}/></button></div></div>
 <div className="graph-viewport" onPointerDown={e=>{if(e.button!==0)return;drag.current={x:e.clientX,y:e.clientY,ox:offset.x,oy:offset.y,moving:false};e.currentTarget.setPointerCapture(e.pointerId)}} onPointerMove={e=>{if(!drag.current)return;const dx=e.clientX-drag.current.x,dy=e.clientY-drag.current.y;if(Math.abs(dx)+Math.abs(dy)>5)drag.current.moving=true;setOffset({x:drag.current.ox+dx,y:drag.current.oy+dy})}} onPointerUp={e=>{drag.current=null;if(e.currentTarget.hasPointerCapture(e.pointerId))e.currentTarget.releasePointerCapture(e.pointerId)}} onPointerCancel={()=>drag.current=null}>
 <div className="graph-stage" style={{width,height,transform:`translate(${offset.x}px,${offset.y}px) scale(${zoom})`,transformOrigin:"top left"}}>
 <svg className="graph-edges" width={width} height={height} aria-hidden="true">{edges.map(({from,to})=>{const a=pos(lookup.get(from)!),b=pos(lookup.get(to)!);const x1=a.x+W,y1=a.y+H/2,x2=b.x,y2=b.y+H/2;return <path key={from+to} d={`M ${x1} ${y1} C ${x1+35} ${y1}, ${x2-35} ${y2}, ${x2} ${y2}`} className="edge"/>})}</svg>
 {nodes.map(n=>{const p=pos(n);return <button key={n.id} type="button" className={"graph-node"+(active===n.id?" active":"")} style={{left:p.x,top:p.y,width:W,height:H}} onPointerDown={e=>e.stopPropagation()} onClick={()=>onSelect(n.id)}><span className="graph-node-label">{String(n.stage+1).padStart(2,"0")} · {String.fromCharCode(65+n.lane)}</span><strong>{n.title}</strong><span className="graph-node-state">ОТКРЫТЬ ↗</span></button>})}
 </div></div></div>
}