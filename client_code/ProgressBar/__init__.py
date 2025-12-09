# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
__version__ = "3.6.1"

css = """ .anvil-role-ae-progress-track, .anvil-role-ae-progress-indicator {
    display: block;
    margin: 0;
}

.anvil-role-ae-progress-track {
    width: 100%;
}

.anvil-role-ae-indeterminate-progress-indicator, .anvil-role-ae-indeterminate-progress-indicator:before {
  width: 100%;
  margin: 0;
}

.anvil-role-ae-indeterminate-progress-indicator {
  display: -webkit-flex;
  display: flex;
}

.anvil-role-ae-indeterminate-progress-indicator:before {
  content: '';
  -webkit-animation: ae-running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  animation: ae-running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  background-color: var(--ae-track-colour);
}

@-webkit-keyframes ae-running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}

@keyframes ae-running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}
"""
