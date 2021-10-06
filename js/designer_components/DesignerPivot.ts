import { DesignerComponent } from "./DesignerComponent.ts";

export class DesignerPivot extends DesignerComponent {
    static links = ["https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css"];
    static scripts = [
        "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js"
    ];
    static init() {
        super.init(".pivot-placeholder");
    }
    constructor(domNode, pyComponent, el) {
        super(domNode, pyComponent, el);
        this.pivot = $(domNode.querySelector(".anvil-extras-pivot"));
    }
    update({rows, columns: cols, values: vals, aggregator: aggregatorName}) {
        const keys = [...rows, ...cols, ...vals, ...['key A', 'key B', 'key C']];
        const item = Object.fromEntries(keys.map(key => [key, 1]));
        this.pivot.pivotUI([item], {rows, cols, vals, aggregatorName}, true);
      }
}
