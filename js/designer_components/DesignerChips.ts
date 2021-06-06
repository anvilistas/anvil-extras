import { DesignerComponent } from "./DesignerComponent.ts";

declare var Sk: any;

export class DesignerChip extends DesignerComponent {
    static css = `.anvil-extras-chip{height:32px;font-size:14px;font-weight:500;color:rgba(0,0,0,0.6);line-height:32px;padding:0 12px;border-radius:16px;background-color:#e4e4e4;cursor:pointer;display:flex;gap:14px;align-items:center;width:fit-content;padding-left:12px;padding-right:12px}.anvil-extras-chip i.anvil-component-icon.left{font-size:1.5rem}.anvil-extras-chip a{user-select:none}.anvil-extras-chip a .link-text{}.anvil-extras-chip span{padding:0 !important}`;
    static init() {
        super.init(".chip-placeholder", "anvil-extras-chip");
    }
    label: any;
    link: any;
    linkNode: HTMLElement;
    constructor(container: HTMLElement, pyComponent: any, temp: HTMLElement) {
        super(container, pyComponent, temp);
        temp.remove();
        this.label = pyComponent._anvil.components[0].component;
        this.link = pyComponent._anvil.components[1].component;
        this.linkNode = this.link._anvil.domNode;
        this.linkNode.classList.remove("anvil-container");
    }
    setProp(propName: string, propVal: any, props: any) {
        switch (propName) {
            case "visible":
                this.updateVisible(props);
                break;
            case "spacing_above":
            case "spacing_below":
                this.updateSpacing(props);
                break;
            case "text":
            case "icon":
                this.label._anvil.setPropJS(propName, propVal);
                break;
            case "foreground":
                this.link._anvil.setPropJS(propName, propVal || "rgba(0,0,0,0.6)");
                this.label._anvil.setPropJS(propName, propVal || "rgba(0,0,0,0.6)");
                break;
            case "close_icon":
                this.linkNode.style.display = propVal ? "block" : "none";
                break;
            case "background":
                this.pyComponent._anvil.setPropJS(propName, propVal);
                break;
        }
    }

    get [Symbol.toStringTag]() {
        return "Chip";
    }
}

export class DesignerChipsInput extends DesignerComponent {
    static css = `.anvil-extras-chips-input input{box-shadow:none !important;border:none !important;padding:7px 0 !important;margin-bottom:0 !important;flex:1;min-width:50px}.anvil-extras-chips-input{display:flex;flex-wrap:wrap;gap:8px;border-bottom:1px solid;align-items:center;padding-bottom:4px}`;
    static init() {
        DesignerChip.init();
        super.init(".chips-input-placeholder", "anvil-extras-chips-input");
    }
    chipNode: HTMLElement;
    input: any;
    inputNode: HTMLElement;
    chips: HTMLElement[];
    constructor(container: HTMLElement, pyComponent: any, temp: HTMLElement) {
        super(container, pyComponent, temp);
        temp.remove();
        const tempChip = pyComponent._anvil.components[0].component;
        this.chipNode = tempChip._anvil.domNode;
        this.input = pyComponent._anvil.components[1].component;
        this.inputNode = this.input._anvil.domNode;
        this.chips = [];
        Sk.misceval.callsimArray(tempChip.tp$getattr(new Sk.builtin.str("remove_from_parent")));
    }
    setProp(propName: string, propVal: any, props: any) {
        switch (propName) {
            case "chips":
                debugger;
                propVal = Array.from(new Set((propVal || []).filter((t) => t)));
                this.chips.forEach((chip) => this.domNode.removeChild(chip));
                this.chips = [];
                propVal.forEach((text, i) => {
                    const newNode = this.chipNode.cloneNode(true);
                    newNode.querySelector("span").textContent = text;
                    this.chips.push(newNode);
                    this.domNode.insertBefore(newNode, this.inputNode);
                });
                this.chips.length
                    ? this.input._anvil.setPropJS("placeholder", props.secondary_placeholder)
                    : this.input._anvil.setPropJS("placeholder", props.primary_placeholder);
                break;
            case "spacing_above":
            case "spacing_below":
                this.updateSpacing(props);
                break;
            case "visible":
                this.updateVisible(props);
                break;
            case "primary_placeholder":
                !this.chips.length && this.input._anvil.setPropJS("placeholder", propVal);
                break;
            case "secondary_placeholder":
                this.chips.length && this.input._anvil.setPropJS("placeholder", propVal);
                break;
        }
    }

    get [Symbol.toStringTag]() {
        return "ChipsInput";
    }
}
