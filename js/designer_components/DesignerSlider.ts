import { DesignerComponent } from "./DesignerComponent.ts";

//deno-lint-ignore
declare var noUiSlider: any;

//deno-lint-ignore
declare var Sk: any;
export interface Slider extends HTMLElement {
    noUiSlider: any;
}

interface Formatter {
    to: (value: number) => string | number;
    from: (value: string) => number | false;
}

const BAR_COLOR = "--slider-bar-color";
const BAR_HEIGHT = "--slider-height";
const HANDLE_SIZE = "--slider-handle-size";
export class DesignerSlider extends DesignerComponent {
    static defaults = {
        start: [20, 80],
        connect: true,
        min: 0,
        max: 100,
        visible: true,
        enabled: true,
    };
    static links = ["https://cdn.jsdelivr.net/npm/nouislider@15.4.0/dist/nouislider.css"];
    static scripts = ["https://cdn.jsdelivr.net/npm/nouislider@15.4.0/dist/nouislider.js"];
    static css = `.anvil-slider-container{padding:10px 0}.anvil-slider-container.has-pips{padding-bottom:40px}
    .anvil-container-overflow,.anvil-panel-col{overflow:visible}.noUi-connect{background:var(${BAR_COLOR})}
    .noUi-horizontal{height:var(${BAR_HEIGHT})}
    .noUi-horizontal .noUi-handle{width:var(${HANDLE_SIZE});height:var(${HANDLE_SIZE});right:calc(var(${HANDLE_SIZE}) / -2);top:calc((-2px + var(${BAR_HEIGHT}) - var(${HANDLE_SIZE}))/2);border-radius:50%}
    .noUi-handle::after,.noUi-handle::before{content:none}`;
    static init() {
        super.init(".anvil-slider", "anvil-slider-container");
    }

    slider: Slider;
    constructor(domNode: HTMLElement, pyComponent: any, slider: Slider) {
        super(domNode, pyComponent, slider);
        this.slider = slider;
    }

    parse(val: any, forceList = false) {
        if (typeof val !== "string") {
            return val;
        }
        val = val.toLowerCase().trim();
        if (!val) return forceList ? [] : null;
        try {
            return JSON.parse((forceList || val.includes(",")) && val[0] !== "[" ? `[${val}]` : val);
        } catch {
            return forceList ? [] : val;
        }
    }
    getFormatter(formatspec: string): Formatter {
        const first = formatspec.indexOf("{");
        const last = formatspec.indexOf("}");
        const prefix = first === -1 ? "" : formatspec.slice(0, first);
        const suffix = last === -1 ? "" : formatspec.slice(last + 1);
        const type = formatspec[last - 1] === "%" ? "%" : null;

        const pyformatspec = Sk.ffi.toPy(formatspec) as any;
        const format = pyformatspec.tp$getattr(Sk.ffi.toPy("format"));

        const doTo = (f: number): any => {
            const pyNum = Sk.ffi.toPy(f);
            return first === -1 ? Sk.builtin.format(pyNum, pyformatspec) : format.tp$call([pyNum]);
        };

        try {
            doTo(1.1);
        } catch (e: any) {
            throw new Error(e.toString());
        }

        return {
            to: (f: number): string | number => {
                try {
                    return doTo(f);
                } catch {
                    return f;
                }
            },
            from: (s: string): number => {
                if (s.startsWith(prefix)) {
                    s = s.slice(prefix.length);
                }
                if (s.endsWith(suffix)) {
                    s = s.slice(0, s.length - suffix.length);
                }
                const hasPercent = type === "%" && s.endsWith("%");
                s = s.trim().replace(/[,_]/g, "");
                let f = parseFloat(s);
                if (hasPercent) {
                    f = f / 100;
                }
                return f;
            },
        };
    }
    update(props: any) {
        try {
            for (const prop of ["start", "connect", "margin", "padding", "limit", "pips_values"]) {
                props[prop] = this.parse(props[prop], prop === "pips_values");
            }
            props.range = { min: props.min, max: props.max };
            props.format = this.getFormatter(props.format || ".2f");

            if (props.pips) {
                props.pips = {
                    format: props["format"],
                    mode: props["pips_mode"],
                    values: props["pips_values"],
                    density: props["pips_density"],
                    stepped: props["pips_stepped"],
                };
            }

            this.domNode.classList.toggle("has-pips", !!props.pips);
            this.slider.noUiSlider?.destroy();
            if (this.slider.firstElementChild) {
                this.slider.removeChild(this.slider.firstElementChild);
            }
            this.domNode.style.setProperty(BAR_COLOR, this.getColor(props.color, true));
            this.updateSpacing(props);
            this.updateVisible(props);
            this.updateRole(props);
            const barHeight = this.getCssLength(props.bar_height || 18);
            const handleSize = this.getCssLength(props.handle_size || 34);
            this.domNode.style.setProperty(BAR_HEIGHT, barHeight);
            this.domNode.style.setProperty(HANDLE_SIZE, handleSize);
            props.enabled ? this.slider.removeAttribute("disabled") : this.slider.setAttribute("disabled", "");
            noUiSlider.create(this.slider, props);
        } catch (e) {
            this.slider.noUiSlider?.destroy();
            if (this.slider.firstElementChild) {
                this.slider.removeChild(this.slider.firstElementChild);
            }
            const invalidComponent = $(`<div class='invalid-component'>
              <i class="glyphicon glyphicon-remove"></i>
              <div class="err">${e.message.replaceAll("noUiSlider", "Slider")}</div></div>`);
            this.slider.appendChild(invalidComponent[0]);
        }
    }

    get [Symbol.toStringTag]() {
        return "Slider";
    }
}
