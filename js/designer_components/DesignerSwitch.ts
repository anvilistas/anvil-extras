import { DesignerComponent } from "./DesignerComponent.ts";
//deno-lint-ignore
declare var Sk: any;
export class DesignerSwitch extends DesignerComponent {
    static css = `
.switch,.switch *{-webkit-tap-highlight-color:transparent;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}
.switch label{cursor:pointer}
.switch label input[type=checkbox]{opacity:0;width:0;height:0}.switch label input[type=checkbox]:checked+.lever{background-color:rgba(var(--color), .5)}
.switch label input[type=checkbox]:checked+.lever:after,.switch label input[type=checkbox]:checked+.lever:before{left:18px}
.switch label input[type=checkbox]:checked+.lever:after{background-color:rgb(var(--color))}
.switch label .lever{content:"";display:inline-block;position:relative;width:36px;height:14px;background-color:rgba(0,0,0,0.38);border-radius:15px;margin-right:10px;-webkit-transition:background 0.3s ease;transition:background 0.3s ease;vertical-align:middle;margin:0 16px}
.switch label .lever:after,.switch label .lever:before{content:"";position:absolute;display:inline-block;width:20px;height:20px;border-radius:50%;left:0;top:-3px;-webkit-transition:left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease}
.switch label .lever:before{background-color:rgb(var(--color), 0.15)}
.switch label .lever:after{background-color:#F1F1F1;-webkit-box-shadow:0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12);box-shadow:0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12)}
input[type=checkbox]:checked:not(:disabled) ~ .lever:active::before,input[type=checkbox]:checked:not(:disabled).tabbed:focus ~ .lever::before{-webkit-transform:scale(2.4);transform:scale(2.4);background-color:rgb(var(--color), 0.15)}
input[type=checkbox]:not(:disabled) ~ .lever:active:before,input[type=checkbox]:not(:disabled).tabbed:focus ~ .lever::before{-webkit-transform:scale(2.4);transform:scale(2.4);background-color:rgba(0,0,0,0.08)}
.switch input[type=checkbox][disabled]+.lever{cursor:default;background-color:rgba(0,0,0,0.12)}
.switch label input[type=checkbox][disabled]+.lever:after,.switch label input[type=checkbox][disabled]:checked+.lever:after{background-color:#949494}`;

    static init() {
        super.init(".anvil-extras-switch");
    }

    cb: any;
    cbNode: HTMLInputElement;
    textNodePre: Text;
    textNodePost: Text;
    constructor(domNode: HTMLElement, pyComponent: any, el: HTMLElement) {
        super(domNode, pyComponent, el);
        const cb = pyComponent._anvil.components[0].component;
        const cbNode = cb._anvil.domNode;
        cbNode.classList.add("switch");
        cbNode.style.setProperty("--color", this.getColorRGB("#2196F3"));
        const span = cbNode.querySelector("span");
        span.classList.add("lever");
        span.removeAttribute("style");
        const label = cbNode.querySelector("label");
        const textNodePre = document.createTextNode("");
        const textNodePost = document.createTextNode("");
        label.prepend(textNodePre);
        label.append(textNodePost);
        label.style.padding = "7px 0";

        this.cb = cb;
        this.cbNode = cbNode;
        this.textNodePre = textNodePre;
        this.textNodePost = textNodePost;
    }

    setProp(propName: string, v: any, props: any) {
        try {
            this.cb._anvil.setProp(propName, Sk.ffi.toPy(v));
        } catch (e) {
            if (propName === "checked_color") {
                this.cbNode.style.setProperty("--color", this.getColorRGB(v, true));
            } else if (propName === "text_pre") {
                this.textNodePre.textContent = v;
            } else {
                this.textNodePost.textContent = v;
            }
        }
    }

    get [Symbol.toStringTag]() {
        return "Switch";
    }
}
