"use client";

import { useEffect, useRef } from "react";
import mermaid from "mermaid";

export default function MermaidDiagram({ chart }: { chart: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false });

    if (ref.current && chart) {
      ref.current.innerHTML = chart;
      mermaid.run({ nodes: [ref.current] });
    }
  }, [chart]);

  return (
    <div className="bg-white border rounded-xl p-4 overflow-x-auto">
      <div ref={ref} className="mermaid" />
    </div>
  );
}