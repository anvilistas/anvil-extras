import { DesignerComponent } from "./DesignerComponent.ts";
export class DesignerMultiSelectDropDown extends DesignerComponent {
    static defaults = {
        placeholder: "None Selected",
        enabled: true,
        visible: true,
        width: "",
        spacing_above: "small",
        spacing_below: "small",
    };
    static links = ["https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/css/bootstrap-select.min.css"];
    static scripts = ["https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/js/bootstrap-select.min.js"];
    static postLoad() {
        // deno-lint-ignore
        $.fn.selectpicker.Constructor.BootstrapVersion = "3";
    }
    static init() {
        super.init(".select-picker");
    }
    picker: JQuery;
    constructor(domNode: HTMLElement, pyComponent: any, select: HTMLElement) {
        super(domNode, pyComponent, select);
        this.picker = $(select);
        this.picker.selectpicker();
    }
    update(this: any, props: any, propName: string) {
        if (propName && !(propName in this.constructor.defaults)) {
            return;
        }
        this.picker.attr("title", props["placeholder"] || null);
        this.picker.selectpicker({ title: props["placeholder"] });
        this.picker.data("width", props["width"]);
        this.picker.attr("disabled", props["enabled"] ? null : "");
        this.updateSpacing(props);
        this.updateVisible(props);
        this.picker.selectpicker("refresh");
        this.picker.selectpicker("render");
    }

    get [Symbol.toStringTag]() {
        return "MultiSelectDropDown";
    }
}
