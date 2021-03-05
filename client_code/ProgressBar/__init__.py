__version__ = "0.1.6"

css = """ .anvil-role-progress-track, .anvil-role-progress-indicator {
    display: block;
    height: 3px;
    margin: 0;
}

.anvil-role-progress-track {
    width: 100%;
}

.anvil-role-progress-indicator {
    top: 0 !important;
}

.anvil-role-progress-track > .holder, .anvil-role-progress-indicator > .holder {
    display: block !important;
}

.anvil-role-indeterminate-progress-indicator, .anvil-role-indeterminate-progress-indicator:before {
  height: 3px;
  width: 100%;
  margin: 0;
}

.anvil-role-indeterminate-progress-indicator {
  display: -webkit-flex;
  display: flex;
}

.anvil-role-indeterminate-progress-indicator:before {
  content: '';
  -webkit-animation: running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  animation: running-progress 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@-webkit-keyframes running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}

@keyframes running-progress {
  0% { margin-left: 0px; margin-right: 100%; }
  50% { margin-left: 25%; margin-right: 0%; }
  100% { margin-left: 100%; margin-right: 0; }
}
"""
