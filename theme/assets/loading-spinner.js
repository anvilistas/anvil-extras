function _rgbToHsl(r, g, b) {
    (r /= 255), (g /= 255), (b /= 255);
    const max = Math.max(r, g, b),
        min = Math.min(r, g, b);
    let h,
        s,
        l = (max + min) / 2;
    if (max === min) {
        h = s = 0; // achromatic
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }
    return [h * 360, s * 100, l * 100];
}

function _loadingSpinnerColor(rgb) {
    rgb = rgb.replace("#", "");
    const _rgb = (i) => parseInt(rgb.substr(i * 2, 2), 16);
    let [h, s, _] = _rgbToHsl(_rgb(0), _rgb(1), _rgb(2));
    h = Math.trunc(h - 206);
    s = 100 + s - 89;
    const L = document.createElement("style");
    L.textContent = `#loadingSpinner, .plotly-loading-spinner {filter: hue-rotate(${h}deg) saturate(${s}%);}`;
    document.head.appendChild(L);
}

_loadingSpinnerColor(document.currentScript.getAttribute("color"));
