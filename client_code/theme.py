# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil

__version__ = "3.0.0"

M3_DEFAULT_SCHEMES = {
    "Material": {
        "dark": {
            "On Primary": "#381E72",
            "Primary": "#D0BCFF",
            "Primary Container": "#4F378B",
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
            "Surface": "#111412",
            "On Background": "#E1E3DF",
            "On Surface": "#C5C7C3",
            "Surface Variant": "#404943",
            "On Surface Variant": "#C0C9C1",
            "Outline": "#8A938C",
            "Dark Overlay 1": "rgba(230, 224, 233, 0.08)",
            "Dark Overlay 2": "rgba(230, 224, 233, 0.12)",
            "Light Overlay 1": "rgba(230, 224, 233, 0.08)",
            "Light Overlay 2": "rgba(230, 224, 233, 0.12)",
            "Disabled Container": "rgba(230, 224, 233, 0.12)",
            "On Disabled": "rgba(230, 224, 233, 0.38)",
            "Primary Overlay 1": "rgba(208, 188, 255, 0.05)",
            "Primary Overlay 2": "rgba(208, 188, 255, 0.08)",
            "Primary Overlay 3": "rgba(208, 188, 255, 0.11)",
            "Outline Variant": "#49454F",
            "On Error": "#601410",
            "Surface Container Low": "#1D1B20",
            "Surface Container Highest": "#36343B",
            "Disabled Container 2": "rgba(230, 224, 233, 0.04)",
            "Error Overlay 1": "rgba(242, 184, 181, 0.08)",
            "Error Overlay 2": "rgba(242, 184, 181, 0.12)",
            "Dark Overlay 3": "rgba(230, 224, 233,0.16)",
            "On Error Container": "#F9DEDC",
            "Surface Container": "#211F26",
            "Inverse Surface": "#E6E0E9",
            "Inverse On Surface": "#322F35",
            "On Surface Variant Overlay 1": "rgba(202,196,208, 0.08)",
            "On Surface Variant Overlay 2": "rgba(202,196,208, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(50,47,53, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(50,47,53, 0.12)",
            "Surface Container High": "#2B2930",
        },
        "light": {
            "On Primary": "#FFFFFF",
            "Primary": "#6750A4",
            "Primary Container": "#EADDFF",
            "On Primary Container": "#21005E",
            "Secondary": "#625B71",
            "Secondary Container": "#E8DEF8",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#1D192B",
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
            "Dark Overlay 1": "rgba(29, 25, 43, 0.08)",
            "Dark Overlay 2": "rgba(29, 25, 43, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Disabled Container": "rgba(29, 27, 32, 0.12)",
            "On Disabled": "rgba(29, 27, 32, 0.38)",
            "Primary Overlay 1": "rgba(103, 80, 164, 0.05)",
            "Primary Overlay 2": "rgba(103, 80, 164, 0.08)",
            "Primary Overlay 3": "rgba(103, 80, 164, 0.12)",
            "Outline Variant": "#C4C7C5",
            "On Error": "#FFFFFF",
            "Surface Container Low": "#F7F2FA",
            "Surface Container Highest": "#E6E0E9",
            "Disabled Container 2": "rgba(29, 27, 32, 0.04)",
            "Error Overlay 1": "rgba(179, 38, 30, 0.08)",
            "Error Overlay 2": "rgba(179, 38, 30, 0.12)",
            "Dark Overlay 3": "rgba(29, 25, 43, 0.16)",
            "On Error Container": "#410E0B",
            "Surface Container": "#F3EDF7",
            "Inverse Surface": "#322F35",
            "Inverse On Surface": "#F5EFF7",
            "On Surface Variant Overlay 1": "rgba(73,69,79, 0.08)",
            "On Surface Variant Overlay 2": "rgba(73,69,79, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(245,239,247, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(245,239,247, 0.12)",
            "Surface Container High": "#ECE6F0",
        },
    },
    "Rally": {
        "dark": {
            "On Primary": "#003824",
            "Primary": "#70DBA7",
            "Primary Container": "#005235",
            "On Primary Container": "#8DF7C2",
            "Secondary": "#B4CCBC",
            "Secondary Container": "#364B3F",
            "On Secondary": "#20352A",
            "On Secondary Container": "#D0E8D8",
            "Tertiary": "#A4CDDD",
            "Tertiary Container": "#234C5A",
            "On Tertiary": "#063542",
            "On Tertiary Container": "#C0E9FA",
            "Error": "#FFB4AB",
            "Background": "#111412",
            "Surface": "#111412",
            "On Background": "#E1E3DF",
            "On Surface": "#C5C7C3",
            "Surface Variant": "#404943",
            "On Surface Variant": "#C0C9C1",
            "Outline": "#8A938C",
            "Dark Overlay 1": "rgba(208, 232, 216, 0.08)",
            "Dark Overlay 2": "rgba(208, 232, 216, 0.12)",
            "Light Overlay 1": "rgba(208, 232, 216, 0.08)",
            "Light Overlay 2": "rgba(208, 232, 216, 0.12)",
            "Disabled Container": "rgba(225, 227, 223, 0.12)",
            "On Disabled": "rgba(225, 227, 223, 0.38)",
            "Primary Overlay 1": "rgba(112, 219, 167, 0.05)",
            "Primary Overlay 2": "rgba(112, 219, 167, 0.08)",
            "Primary Overlay 3": "rgba(112, 219, 167, 0.11)",
            "Outline Variant": "#404943",
            "On Error": "#690005",
            "Surface Container Low": "#191C1A",
            "Surface Container Highest": "#323633",
            "Disabled Container 2": "rgba(225, 227, 223, 0.04)",
            "Error Overlay 1": "rgba(255, 180, 171, 0.08)",
            "Error Overlay 2": "rgba(255, 180, 171, 0.12)",
            "Dark Overlay 3": "rgba(208, 232, 216, 0.16)",
            "On Error Container": "#FFDAD6",
            "Surface Container": "#1D201E",
            "Inverse Surface": "#E1E3DF",
            "Inverse On Surface": "#191C1A",
            "On Surface Variant Overlay 1": "rgba(192,201,193, 0.08)",
            "On Surface Variant Overlay 2": "rgba(192,201,193, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(25,28,26, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(25,28,26, 0.12)",
            "Surface Container High": "#262B27",
        },
        "light": {
            "On Primary": "#FFFFFF",
            "Primary": "#006C48",
            "Primary Container": "#8DF7C2",
            "On Primary Container": "#002113",
            "Secondary": "#4D6356",
            "Secondary Container": "#D0E8D8",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#0A1F15",
            "Tertiary": "#3C6472",
            "Tertiary Container": "#C0E9FA",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#001F28",
            "Error": "#BA1A1A",
            "Background": "#FBFDF8",
            "Surface": "#F8FAF6",
            "On Background": "#191C1A",
            "On Surface": "#191C1A",
            "Surface Variant": "#DCE5DD",
            "On Surface Variant": "#404943",
            "Outline": "#707973",
            "Dark Overlay 1": "rgba(10, 31, 21, 0.08)",
            "Dark Overlay 2": "rgba(10, 31, 21, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Disabled Container": "rgba(25, 28, 26, 0.12)",
            "On Disabled": "rgba(25, 28, 26, 0.38)",
            "Primary Overlay 1": "rgba(0, 108, 72, 0.05)",
            "Primary Overlay 2": "rgba(0, 108, 72, 0.08)",
            "Primary Overlay 3": "rgba(0, 108, 72, 0.11)",
            "Outline Variant": "#C0C9C1",
            "On Error": "#FFFFFF",
            "Surface Container Low": "#F2F4F0",
            "Surface Container Highest": "#E1E3DF",
            "Disabled Container 2": "rgba(25, 28, 26, 0.04)",
            "Error Overlay 1": "rgba(186, 26, 26, 0.08)",
            "Error Overlay 2": "rgba(186, 26, 26, 0.12)",
            "Dark Overlay 3": "rgba(10, 31, 21, 0.16)",
            "On Error Container": "#410002",
            "Surface Container": "#ECEEEA",
            "Inverse Surface": "#2E312F",
            "Inverse On Surface": "#EFF1ED",
            "On Surface Variant Overlay 1": "rgba(25,28,26, 0.08)",
            "On Surface Variant Overlay 2": "rgba(25,28,26, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(239,241,237, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(239,241,237, 0.12)",
            "Surface Container High": "#E4EAE3",
        },
    },
    "Mykonos": {
        "dark": {
            "On Primary": "#00363D",
            "Primary": "#3CD9ED",
            "Primary Container": "#004F57",
            "On Primary Container": "#96F0FF",
            "Secondary": "#B1CBD0",
            "Secondary Container": "#334B4F",
            "On Secondary": "#1C3438",
            "On Secondary Container": "#CDE7EC",
            "Tertiary": "#BAC6EA",
            "Tertiary Container": "#3B4664",
            "On Tertiary": "#24304D",
            "On Tertiary Container": "##DAE2FF",
            "Error": "#FFB4AB",
            "Background": "#101415",
            "Surface": "#101415",
            "On Background": "#E1E3E3",
            "On Surface": "#C4C7C7",
            "Surface Variant": "#3F484A",
            "On Surface Variant": "#BFC8CA",
            "Outline": "#899294",
            "Dark Overlay 1": "rgba(203, 232, 237, 0.08)",
            "Dark Overlay 2": "rgba(203, 232, 237, 0.12)",
            "Light Overlay 1": "rgba(203, 232, 237, 0.08)",
            "Light Overlay 2": "rgba(203, 232, 237, 0.12)",
            "Disabled Container": "rgba(225, 227, 227, 0.12)",
            "On Disabled": "rgba(225, 227, 227, 0.38)",
            "Primary Overlay 1": "rgba(60, 217, 237, 0.05)",
            "Primary Overlay 2": "rgba(60, 217, 237, 0.08)",
            "Primary Overlay 3": "rgba(60, 217, 237, 0.11)",
            "Outline Variant": "#3F484A",
            "On Error": "#690005",
            "Surface Container Low": "#191C1D",
            "Surface Container Highest": "#323536",
            "Disabled Container 2": "rgba(225, 227, 227, 0.04)",
            "Error Overlay 1": "rgba(255, 180, 171, 0.08)",
            "Error Overlay 2": "rgba(255, 180, 171, 0.12)",
            "Dark Overlay 3": "rgba(203, 232, 237, 0.16)",
            "On Error Container": "#FFDAD6",
            "Surface Container": "#1D2021",
            "Inverse Surface": "#E1E3E3",
            "Inverse On Surface": "#191C1D",
            "On Surface Variant Overlay 1": "rgba(191,200,202, 0.08)",
            "On Surface Variant Overlay 2": "rgba(191,200,202, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(25,28,29, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(25,28,29, 0.12)",
            "Surface Container High": "#252B2C",
        },
        "light": {
            "On Primary": "#FFFFFF",
            "Primary": "#006874",
            "Primary Container": "#96F0FF",
            "On Primary Container": "#001F24",
            "Secondary": "#4A6267",
            "Secondary Container": "#CDE7EC",
            "On Secondary": "#FFFFFF",
            "On Secondary Container": "#051F23",
            "Tertiary": "#535E7E",
            "Tertiary Container": "#DAE2FF",
            "On Tertiary": "#FFFFFF",
            "On Tertiary Container": "#0F1A37",
            "Error": "#BA1A1A",
            "Background": "#FBFCFD",
            "Surface": "#F8FAFA",
            "On Background": "#191C1D",
            "On Surface": "#191C1D",
            "Surface Variant": "#DBE4E6",
            "On Surface Variant": "#3F484A",
            "Outline": "#6F797A",
            "Dark Overlay 1": "rgba(3, 31, 35, 0.08)",
            "Dark Overlay 2": "rgba(3, 31, 35, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Disabled Container": "rgba(25, 28, 29, 0.12)",
            "On Disabled": "rgba(25, 28, 29, 0.38)",
            "Primary Overlay 1": "rgba(0, 104, 116, 0.05)",
            "Primary Overlay 2": "rgba(0, 104, 116, 0.08)",
            "Primary Overlay 3": "rgba(0, 104, 116, 0.11)",
            "Outline Variant": "#BFC8CA",
            "On Error": "#FFFFFF",
            "Surface Container Low": "#F2F4F4",
            "Surface Container Highest": "#E1E3E3",
            "Disabled Container 2": "rgba(25, 28, 29, 0.04)",
            "Error Overlay 1": "rgba(186, 26, 26, 0.08)",
            "Error Overlay 2": "rgba(186, 26, 26, 0.12)",
            "Dark Overlay 3": "rgba(3, 31, 35, 0.16)",
            "On Error Container": "#410002",
            "Surface Container": "#ECEEEF",
            "Inverse Surface": "#2E3132",
            "Inverse On Surface": "#EFF1F1",
            "On Surface Variant Overlay 1": "rgba(219,228,230, 0.08)",
            "On Surface Variant Overlay 2": "rgba(219,228,230, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(239,241,241, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(239,241,241, 0.12)",
            "Surface Container High": "#E3E9EA",
        },
    },
    "Manarola": {
        "dark": {
            "On Primary": "#5B1A00",
            "Primary": "#FFB59B",
            "Primary Container": "#7B2E0E",
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
            "Background": "#181210",
            "Surface": "#181210",
            "On Background": "#EDE0DC",
            "On Surface": "#D0C4C0",
            "Surface Variant": "#53433E",
            "On Surface Variant": "#D8C2BB",
            "Outline": "#A08D86",
            "Dark Overlay 1": "rgba(255, 219, 207, 0.08)",
            "Dark Overlay 2": "rgba(255, 219, 207, 0.12)",
            "Light Overlay 1": "rgba(255, 219, 207, 0.08)",
            "Light Overlay 2": "rgba(255, 219, 207, 0.12)",
            "Disabled Container": "rgba(237, 224, 220, 0.12)",
            "On Disabled": "rgba(237, 224, 220, 0.38)",
            "Primary Overlay 1": "rgba(255, 181, 155, 0.05)",
            "Primary Overlay 2": "rgba(255, 181, 155, 0.08)",
            "Primary Overlay 3": "rgba(255, 181, 155, 0.11)",
            "Outline Variant": "#53433E",
            "On Error": "#690005",
            "Surface Container Low": "#201A18",
            "Surface Container Highest": "#3B3331",
            "Disabled Container 2": "rgba(237, 224, 220, 0.04)",
            "Error Overlay 1": "rgba(255, 180, 171, 0.08)",
            "Error Overlay 2": "rgba(255, 180, 171, 0.12)",
            "Dark Overlay 3": "rgba(255, 219, 207, 0.16)",
            "On Error Container": "#FFDAD6",
            "Surface Container": "#251E1C",
            "Inverse Surface": "#EDE0DC",
            "Inverse On Surface": "#201A18",
            "On Surface Variant Overlay 1": "rgba(216,194,187, 0.08)",
            "On Surface Variant Overlay 2": "rgba(216,194,187, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(32,26,24, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(32,26,24, 0.12)",
            "Surface Container High": "#322824",
        },
        "light": {
            "On Primary": "#FFFFFF",
            "Primary": "#9A4523",
            "Primary Container": "#FFDBCF",
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
            "Background": "#FFF8F6",
            "Surface": "#FFF8F6",
            "On Background": "#201A18",
            "On Surface": "#201A18",
            "Surface Variant": "#F5DED6",
            "On Surface Variant": "#53433E",
            "Outline": "#85736D",
            "Dark Overlay 1": "rgba(44, 22, 13, 0.08)",
            "Dark Overlay 2": "rgba(44, 22, 13, 0.12)",
            "Light Overlay 1": "rgba(255, 255, 255, 0.08)",
            "Light Overlay 2": "rgba(255, 255, 255, 0.12)",
            "Disabled Container": "rgba(32, 26, 24, 0.12)",
            "On Disabled": "rgba(32, 26, 24, 0.38)",
            "Primary Overlay 1": "rgba(154, 69, 35, 0.05)",
            "Primary Overlay 2": "rgba(154, 69, 35, 0.08)",
            "Primary Overlay 3": "rgba(154, 69, 35, 0.11)",
            "Outline Variant": "#D8C2BB",
            "On Error": "#FFFFFF",
            "Surface Container Low": "#FEF1ED",
            "Surface Container Highest": "#EDE0DC",
            "Disabled Container 2": "rgba(32, 26, 24, 0.04)",
            "Error Overlay 1": "rgba(186, 26, 26, 0.08)",
            "Error Overlay 2": "rgba(186, 26, 26, 0.12)",
            "Dark Overlay 3": "rgba(44, 22, 13, 0.16)",
            "On Error Container": "#410002",
            "Surface Container": "#F8EBE7",
            "Inverse Surface": "#362F2C",
            "Inverse On Surface": "#FBEEEA",
            "On Surface Variant Overlay 1": "rgba(83,67,62, 0.08)",
            "On Surface Variant Overlay 2": "rgba(83,67,62, 0.12)",
            "Inverse On Surface Overlay 1": "rgba(32,26,24, 0.08)",
            "Inverse On Surface Overlay 2": "rgba(32,26,24, 0.12)",
            "Surface Container High": "#F7E4DF",
        },
    },
}


class Colors:
    def __init__(self, schemes=None, scheme=None, variant=None):
        self.schemes = schemes or M3_DEFAULT_SCHEMES
        self._scheme = scheme or tuple(self.schemes.keys())[0]
        self._variant = variant or tuple(self.variants[0])
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
