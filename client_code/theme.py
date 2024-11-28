# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil

__version__ = "3.1.0"

M3_DEFAULT_SCHEMES = {
    "Material": {
        "dark": {
            "Primary": "#D0BCFF",
            "Primary Container": "#4F378B",
            "On Primary": "#371E73",
            "On Primary Container": "#EADDFF",
            "Secondary": "#CCC2DC",
            "Secondary Container": "#4A4458",
            "On Secondary": "#332D41",
            "On Secondary Container": "#E8DEF8",
            "Tertiary": "#EFB8C8",
            "Tertiary Container": "#633B48",
            "On Tertiary": "#492532",
            "On Tertiary Container": "#FFD8E4",
            "Error": "#F2B8B5",
            "Background": "#1C1B1F",
            "Surface": "#1C1B1F",
            "On Background": "#E6E1E5",
            "On Surface": "#E6E1E5",
            "Surface Variant": "#49454F",
            "On Surface Variant": "#CAC4D0",
            "Outline": "#938F99",
            "On Disabled": "rgba(230, 225, 229, 0.38)",
            "Disabled Container": "rgba(230, 225, 229, 0.12)",
            "Light Overlay 1": "rgba(232, 222, 248, 0.08)",
            "Light Overlay 2": "rgba(232, 222, 248, 0.12)",
            "Dark Overlay 1": "rgba(232, 222, 248, 0.08)",
            "Dark Overlay 2": "rgba(232, 222, 248, 0.12)",
            "Primary Overlay 1": "rgba(208, 188, 255, 0.05)",
            "Primary Overlay 2": "rgba(208, 188, 255, 0.08)",
            "Primary Overlay 3": "rgba(208, 188, 255, 0.11)",
        },
        "light": {
            "Primary": "#6750A4",
            "Primary Container": "#EADDFF",
            "On Primary": "#FFFFFF",
            "On Primary Container": "#21005E",
            "Secondary": "#625B71",
            "Secondary Container": "#E8DEF8",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#1E192B",
            "Tertiary": "#7D5260",
            "Tertiary Container": "#FFD8E4",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#370B1E",
            "Error": "#B3261E",
            "Background": "#FFFBFE",
            "Surface": "#FFFBFE",
            "On Background": "#1C1B1F",
            "On Surface": "#1C1B1F",
            "Surface Variant": "#E7E0EC",
            "On Surface Variant": "#49454E",
            "Outline": "#79747E",
            "On Disabled": "rgba(28, 27, 31, 0.38)",
            "Disabled Container": "rgba(28, 27, 31, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Dark Overlay 1": "rgba(30, 25, 43, 0.08)",
            "Dark Overlay 2": "rgba(30, 25, 43, 0.12)",
            "Primary Overlay 1": "rgba(103, 80, 164, 0.05)",
            "Primary Overlay 2": "rgba(103, 80, 164, 0.08)",
            "Primary Overlay 3": "rgba(103, 80, 164, 0.11)",
        },
    },
    "Rally": {
        "dark": {
            "Primary": "#1EB980",
            "Primary Container": "#005235",
            "On Primary": "#003824",
            "On Primary Container": "#73FBBC",
            "Secondary": "#B4CCBC",
            "Secondary Container": "#364B3F",
            "On Secondary": "#20352A",
            "On Secondary Container": "#D0E8D8",
            "Tertiary": "#A4CDDD",
            "Tertiary Container": "#234C5A",
            "On Tertiary": "#063542",
            "On Tertiary Container": "#C0E9FA",
            "Error": "#D64D47",
            "Background": "#191C1A",
            "Surface": "#191C1A",
            "On Background": "#E1E3DF",
            "On Surface": "#E1E3DF",
            "Surface Variant": "#404943",
            "On Surface Variant": "#C0C9C1",
            "Outline": "#8A938C",
            "On Disabled": "#85858B",
            "Disabled Container": "rgba(133, 133, 139, 0.12)",
            "Light Overlay 1": "rgba(208, 232, 216, 0.2)",
            "Light Overlay 2": "rgba(208, 232, 216, 0.5)",
            "Dark Overlay 1": "rgba(208, 232, 216, 0.2)",
            "Dark Overlay 2": "rgba(208, 232, 216, 0.5)",
            "Primary Overlay 1": "rgba(30, 185, 128, 0.05)",
            "Primary Overlay 2": "rgba(30, 185, 128, 0.08)",
            "Primary Overlay 3": "rgba(30, 185, 128, 0.11)",
        },
        "light": {
            "Primary": "#006C48",
            "Primary Container": "#00A36C",
            "On Primary": "#FFFFFF",
            "On Primary Container": "#002113",
            "Secondary": "#496455",
            "Secondary Container": "#CBEAD6",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#052014",
            "Tertiary": "#326576",
            "Tertiary Container": "#B8EAFF",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#001F28",
            "Error": "#D64D47",
            "Background": "#FBFDF8",
            "Surface": "#FBFDF8",
            "On Background": "#191C1A",
            "On Surface": "#191C1A",
            "Surface Variant": "#DCE5DD",
            "On Surface Variant": "#404943",
            "Outline": "#707973",
            "On Disabled": "rgba(25, 28, 26, 0.38)",
            "Disabled Container": "rgba(25, 28, 26, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.8)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Dark Overlay 1": "rgba(5, 32, 20, 0.8)",
            "Dark Overlay 2": "rgba(51, 51, 61, 0.12)",
            "Primary Overlay 1": "rgba(0, 108, 72, 0.05)",
            "Primary Overlay 2": "rgba(0, 108, 72, 0.08)",
            "Primary Overlay 3": "rgba(0, 108, 72, 0.11)",
        },
    },
    "Mykonos": {
        "dark": {
            "Primary": "#3CD9ED",
            "Primary Container": "#004F57",
            "On Primary": "#00363D",
            "On Primary Container": "#96F0FF",
            "Secondary": "#AFCBD0",
            "Secondary Container": "#314B4F",
            "On Secondary": "#1A3438",
            "On Secondary Container": "#CBE8ED",
            "Tertiary": "#B9C6ED",
            "Tertiary Container": "#394667",
            "On Tertiary": "#23304F",
            "On Tertiary Container": "#DAE2FF",
            "Error": "#FFB4AB",
            "Background": "#191C1D",
            "Surface": "#191C1D",
            "On Background": "#E1E3E3",
            "On Surface": "#E1E3E3",
            "Surface Variant": "#3F484A",
            "On Surface Variant": "#BFC8CA",
            "Outline": "#899294",
            "On Disabled": "rgba(225, 227, 227, 0.38)",
            "Disabled Container": "rgba(225, 227, 227, 0.12)",
            "Light Overlay 1": "rgba(203, 232, 237, 0.08)",
            "Light Overlay 2": "rgba(203, 232, 237, 0.12)",
            "Dark Overlay 1": "rgba(203, 232, 237, 0.08)",
            "Dark Overlay 2": "rgba(203, 232, 237, 0.12)",
            "Primary Overlay 1": "rgba(60, 217, 237, 0.05)",
            "Primary Overlay 2": "rgba(60, 217, 237, 0.08)",
            "Primary Overlay 3": "rgba(60, 217, 237, 0.11)",
        },
        "light": {
            "Primary": "#006874",
            "Primary Container": "#96F0FF",
            "On Primary": "#FFFFFF",
            "On Primary Container": "#001F24",
            "Secondary": "#486367",
            "Secondary Container": "#CBE8ED",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#031F23",
            "Tertiary": "#515E80",
            "Tertiary Container": "#DAE2FF",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#0C1A39",
            "Error": "#BA1A1A",
            "Background": "#FAFDFD",
            "Surface": "#FAFDFD",
            "On Background": "#191C1D",
            "On Surface": "#191C1D",
            "Surface Variant": "#DBE4E6",
            "On Surface Variant": "#3F484A",
            "Outline": "#6F797A",
            "On Disabled": "rgba(25, 28, 29, 0.38)",
            "Disabled Container": "rgba(25, 28, 29, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Dark Overlay 1": "rgba(3, 31, 35, 0.08)",
            "Dark Overlay 2": "rgba(3, 31, 35, 0.12)",
            "Primary Overlay 1": "rgba(0, 104, 116, 0.05)",
            "Primary Overlay 2": "rgba(0, 104, 116, 0.08)",
            "Primary Overlay 3": "rgba(0, 104, 116, 0.11)",
        },
    },
    "Manarola": {
        "dark": {
            "Primary": "#FFB59B",
            "Primary Container": "#7B2E0E",
            "On Primary": "#5B1A00",
            "On Primary Container": "#FFDBCF",
            "Secondary": "#E7BDB0",
            "Secondary Container": "#5D4036",
            "On Secondary": "#442A21",
            "On Secondary Container": "#FFDBCF",
            "Tertiary": "#D5C68E",
            "Tertiary Container": "#50461A",
            "On Tertiary": "#393005",
            "On Tertiary Container": "#F2E2A7",
            "Error": "#FFB4AB",
            "Background": "#201A18",
            "Surface": "#201A18",
            "On Background": "#EDE0DC",
            "On Surface": "#EDE0DC",
            "Surface Variant": "#53433E",
            "On Surface Variant": "#D8C2BB",
            "Outline": "#A08D86",
            "On Disabled": "rgba(237, 224, 220, 0.38)",
            "Disabled Container": "rgba(237, 224, 220, 0.12)",
            "Light Overlay 1": "rgba(255, 219, 207, 0.08)",
            "Light Overlay 2": "rgba(255, 219, 207, 0.12)",
            "Dark Overlay 1": "rgba(255, 219, 207, 0.08)",
            "Dark Overlay 2": "rgba(255, 219, 207, 0.12)",
            "Primary Overlay 1": "rgba(255, 181, 155, 0.05)",
            "Primary Overlay 2": "rgba(255, 181, 155, 0.08)",
            "Primary Overlay 3": "rgba(255, 181, 155, 0.11)",
        },
        "light": {
            "Primary": "#9A4523",
            "Primary Container": "#FFDBCF",
            "On Primary": "#FFFFFF",
            "On Primary Container": "#380D00",
            "Secondary": "#77574C",
            "Secondary Container": "#FFDBCF",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#2C160D",
            "Tertiary": "#695E2F",
            "Tertiary Container": "#F2E2A7",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#221B00",
            "Error": "#BA1A1A",
            "Background": "#FFFBFF",
            "Surface": "#FFFBFF",
            "On Background": "#201A18",
            "On Surface": "#201A18",
            "Surface Variant": "#F5DED6",
            "On Surface Variant": "#53433E",
            "Outline": "#85736D",
            "On Disabled": "rgba(32, 26, 24, 0.38)",
            "Disabled Container": "rgba(32, 26, 24, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Dark Overlay 1": "rgba(44, 22, 13, 0.08)",
            "Dark Overlay 2": "rgba(44, 22, 13, 0.12)",
            "Primary Overlay 1": "rgba(154, 69, 35, 0.05)",
            "Primary Overlay 2": "rgba(154, 69, 35, 0.08)",
            "Primary Overlay 3": "rgba(154, 69, 35, 0.11)",
        },
    },
}


class Colors:
    def __init__(self, schemes=None, scheme=None, variant=None):
        self.schemes = schemes or M3_DEFAULT_SCHEMES
        self._scheme = scheme or tuple(self.schemes.keys())[0]
        self._variant = variant or self.variants[0]
        self._set_scheme(self.scheme, self.variant)

    def _set_scheme(self, scheme, variant):
        try:
            anvil.app.theme_colors.update(self.schemes[scheme][variant])
        except KeyError:
            raise ValueError(f"{scheme} {variant} is not defined.")

    def set_scheme(self, scheme, variant):
        self._set_scheme(scheme, variant)
        self._scheme = scheme
        self._variant = variant

    @property
    def variants(self):
        return tuple(self.schemes[self._scheme].keys())

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        self._set_scheme(scheme, self.variant)
        self._scheme = scheme

    @property
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, variant):
        self._set_scheme(self.scheme, variant)
        self._variant = variant

    def toggle_variant(self):
        current = self.variants.index(self.variant)
        self.variant = self.variants(not current)
