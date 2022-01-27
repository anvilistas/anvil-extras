

interface Window {
    $: any;
    Sk: any;
}

const HASUNITS = /[a-zA-Z%]/g

/**
 * To create a designer class that supports dynamically updating the design view
 * subclass from DesignerComponent
 * override some static methods/attributes
 * override either update or setProp
 */
export class DesignerComponent {
    /** the css will be injected into the design view. This will match any injected css in your python code */
    static css = "";

    /** If using external links for css override links (see DesignerQuill.ts for example) */
    static links: string[] = [];

    /** If using an external CDN to include a script tag override the script attribute */
    static scripts: string[] = [];
    private static loaded = false;
    private static loading = false;

    /**
     * defaults are used when the component is in its own design view
     * i.e. it's not being used as a custom component
     */
    static defaults: { [keys: string]: any} | null = null;
    private static initializing: boolean = false;

    /** Override this method if you need to do something after script tags have finished loading */
    static postLoad(): void {}


    /**
     *
     * @param domNode The HTMLPanel dom node for this eleemnt
     * @param pyComponent the python HTMLPanel in Javascript (it is a Skulpt object)
     * @param el The first element child dom node of the HTMLpanel
     *
     * You can override the constructor method to add instance attributes
     * based on the paramaters above
     * If you override remember to call super(domNode, pyComponent, el)
     */
    constructor(public domNode: HTMLElement, public pyComponent: any, public el: HTMLElement) {
        this.domNode = domNode;
        this.pyComponent = pyComponent;
        this.el = el;
    }

    /**
     *
     * @param selector The selector should be a class (or other selector) that identifies an immediate child of the HTMLPanel
     * @param className optional - this is primarily used to prevent calling this method multiple times on the same HTMLPanel element.
     * The className will be added to the HTMLPanel at runtime.
     * Use when you want your HTMLPanel to have a class that matches your injected css.
     *
     * e.g.
     * ```ts
     * static init() {
     *     // .chip-placeholder is an immediate child of the HTMLPanel
     *     // anvil-extras-chips is a class added to the HTMLPanel at runtime
     *     super.init(".chip-placeholder", "anvil-extras-chip");
     * }
     * ```
     */
    static init(selector: string, className: string = "anvil-extras-designer") {
        const doInit = () => {
            this.loading = true;
            $(() => {
                this.setup(selector, className);
                this.postLoad();
                this.loaded = true;
                this.loading = false;
            });
        };

        if (!this.loaded && !this.loading) {
            // set this now to prevent other instance trying to do the same thing
            this.loading = true;
            this.links.forEach((href) => {
                const l = document.createElement("link");
                l.href = href;
                l.rel = "stylesheet";
                document.body.appendChild(l);
            });
            if (this.css) {
                // load the css after the link
                const s = document.createElement("style");
                s.innerHTML = this.css;
                document.body.appendChild(s);
            }
            if (this.scripts.length) {
                const promises = this.scripts.map(
                    (script) =>
                        new Promise((resolve, reject) => {
                            const s = document.createElement("script");
                            s.src = script;
                            document.body.appendChild(s);
                            s.onload = resolve;
                            s.onerror = reject;
                        })
                );
                Promise.all(promises).then(doInit);

            } else {
                doInit();
            }
        } else if (!this.loading) {
            doInit();
        }
    }

    private static setup(selector: string, className: string) {
        for (let el of document.querySelectorAll<HTMLElement>(selector)) {
            const container = el.parentElement;
            if (container.classList.contains(className)) {
                return;
            }
            container.classList.add(className);

            const pyComponent = $(container).data("anvilPyComponent");
            let props;
            try {
                props = pyComponent._anvil.customPropVals;
            } catch (e) {
                  console.error(e);
                return;
            }
            const self = new this(container, pyComponent, el);
            if (props) {
                // we are a custom component
                self.makeGetSets(props);
            } else if (this.defaults) {
                // we're in our own design view
                // i.e. we're not being used as a custom component
                // call update()/setProp() using the defaults if they were provided
                self.update({ ...this.defaults });
                for (let [propName, propVal] of Object.entries(this.defaults)) {
                    self.setProp(propName, propVal, this.defaults);
                }
            }
        }
    }

    /** this is where the magic happens. We've intercepted the anvil props object and now we create getters/setters */
    private makeGetSets(props: { [keys: string]: any}): void {
        const copyProps = { ...props };
        const self = this;
        this.update({ ...copyProps });
        for (let propName in copyProps) {
            this.setProp(propName, props[propName], copyProps);
            Object.defineProperty(props, propName, {
                get() {
                    return copyProps[propName];
                },
                set(v) {
                    copyProps[propName] = v;
                    try {
                        self.setProp(propName, v, copyProps);
                        self.update({ ...copyProps }, propName, v);
                    } catch {}
                    return true;
                },
            });
        }
    }

    /**
     * @param {{[propName: string]: any}} props These will be all the current props
     * @param {string?} propName The prop currently being updated (will be undefined on the initial call)
     * @param {any?} val the value the prop will take - will be undefined on the first call
     *
     * either override update or setProp but not both
     * typically use update when you don't mind changing the whole element when a prop changes
     * see DesignerQuill.ts
     */
    public update(props: object, propName?: string, val?: any): void {}

    /**
     * @param propName the name of the prop being updated
     * @param val the value the prop will take
     * @param props All the current props
     *
     * either override update or setProp but not both
     * typically used in a switch case block - see DesignerChips.ts
     */
    public setProp(propName: string, val: any, props: any): void {}

    /** helper method for updating the spacing */
    public updateSpacing({ spacing_above , spacing_below }: { spacing_above: string, spacing_below: string, [keys: string]: any}): void {
        const stale_spacing = Array.prototype.filter.call(this.domNode.classList, (x: string) =>
            x.startsWith("anvil-spacing-")
        );
        this.domNode.classList.remove(...stale_spacing);
        spacing_above && this.domNode.classList.add(("anvil-spacing-above-" + spacing_above) as string);
        spacing_below && this.domNode.classList.add(("anvil-spacing-above-" + spacing_below) as string);
    }

    /** helper method to update the role property when it changes */
    public updateRole({ role }: { role: string, [keys: string]: any}) {
        const stale_role = Array.prototype.filter.call(this.domNode.classList, (x) => x.startsWith("anvil-role-"));
        this.domNode.classList.remove(...stale_role);
        role && this.domNode.classList.add("anvil-role-" + role);
    }

    /** helper method to update the visible property when it changes */
    public updateVisible({ visible }: { visible: boolean, [keys: string]: any}) {
        this.domNode.classList.toggle("visible-false", !visible);
    }

    /** helper method */
    public getColor(color?: string, _default?: string | boolean): string | undefined {
        if (color && color.startsWith("theme:")) {
            //@ts-ignore
            color = window.anvilThemeColors[color.replace("theme:", "")] || "";
        }
        if (!color && _default) {
            if (_default === true || _default === "primary") {
                //@ts-ignore
                return window.anvilThemeColors["Primary 500"] || "#2196F3";
            }
            return _default;
        }
        return color;
    }

    /** helper method */
    public getColorRGB(color?: string, _default?: string | boolean) {
        color = this.getColor(color, _default);
        if (color && color.startsWith("#")) {
            const bigint = parseInt(color.slice(1), 16);
            return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255].join(",");
        } else if (color && color.startsWith("rgb(")) {
            return color.slice(4, color.length - 1);
        }
        return color;
    }

    public getCssLength(len?: string) {
        len ??= "";
        return ("" + len).match(HASUNITS) ? len : len + "px";
    }

    /** helper method for clearing a domnode that will be reinstantiated during an update */
    public clearElement(el: HTMLElement) {
        while (el.firstElementChild) {
            el.removeChild(el.firstElementChild);
        }
    }

    /** useful for debugging */
    get [Symbol.toStringTag]() {
        return "Designer Component";
    }
}
