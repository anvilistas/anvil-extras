// global.d.ts

import { default as _Quill } from "quill";

import _noUiSlider, { API } from "nouislider";

declare var Sk: any;

declare var Quill: typeof _Quill;

export interface Slider extends HTMLElement {
    noUiSlider: API;
}

declare var noUiSlider: typeof _noUiSlider;
