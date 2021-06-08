import { DesignerComponent } from "./DesignerComponent.ts";

export class DesignerTabs extends DesignerComponent {
    static defaults = { tab_titles: ["Tab 1", "Tab 2"], active_tab_index: 0, visible: true, align: "left" };

    static css = `.anvil-extras-tabs.anvil-role-card{border-bottom-left-radius:0;border-bottom-right-radius:0;margin-bottom:-1px}.tabs{position:relative;overflow-x:auto;overflow-y:hidden;height:48px;width:100%;background-color:var(--background, inherit);margin:0 auto;white-space:nowrap;padding:0;display:flex;z-index:1}.tabs .tab{flex-grow:1;display:inline-block;text-align:center;line-height:48px;height:48px;padding:0;margin:0;text-transform:uppercase}.tabs .tab a{color:rgba(var(--color),0.7);display:block;width:100%;height:100%;padding:0 24px;font-size:14px;text-overflow:ellipsis;overflow:hidden;-webkit-transition:color 0.28s ease, background-color 0.28s ease;transition:color 0.28s ease, background-color 0.28s ease}.tabs .tab a:focus,.tabs .tab a:focus.active{background-color:rgb(var(--color), 0.2);outline:none}.tabs .tab a.active,.tabs .tab a:hover{background-color:transparent;color:rgb(var(--color))}.tabs .indicator{position:absolute;bottom:0;height:3px;background-color:rgb(var(--color), 0.4);will-change:left, right}`;

    static init() {
        super.init(".anvil-container .tabs", "anvil-extras-designer");
    }

    tabs: HTMLDivElement;

    // deno-lint-ignore
    constructor(domNode: HTMLElement, pyComponent: any, el: HTMLDivElement) {
        super(domNode, pyComponent, el);
        this.tabs = el;
        this.domNode.style.paddingTop = "0";
        this.domNode.style.paddingBottom = "0";
    }

    update(props: any) {
        this.clearElement(this.tabs);

        let active: any = { offsetLeft: 0, offsetWidth: 0 };
        props.tab_titles ||= [];
        props.tab_titles.forEach((title: string, i: number) => {
            const li = document.createElement("li");
            li.className = "tab";
            const a = document.createElement("a");
            a.style.cssText = `
			font-weight:${props.bold ? "bold" : ""};
			text-align: ${props.align};
			font-size: ${props.font_size ? props.font_size + "px" : ""};
			font-family:${props.font || ""};
			font-style: ${props.italic ? "italic" : ""};
			`;
            a.textContent = title;
            li.appendChild(a);
            this.tabs.appendChild(li);
            if (i === props.active_tab_index) {
                a.className = "active";
                active = li;
            }
        });
        const indicator = document.createElement("li");
        this.tabs.appendChild(indicator);
        indicator.className = "indicator";
        indicator.style.left = active.offsetLeft + "px";
        indicator.style.right = this.tabs.offsetWidth - active.offsetLeft - active.offsetWidth + "px";

        const fg = this.getColorRGB(props.foreground, true);
        this.tabs.style.setProperty("--color", fg);

        const bg = this.getColor(props.background);
        this.tabs.style.setProperty("--background", bg);

        this.updateSpacing(props);
        this.updateRole(props);
        this.updateVisible(props);
    }
    get [Symbol.toStringTag]() {
        return "Tabs";
    }
}
