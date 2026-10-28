# morelkai — standalone Zsh or Oh My Zsh.
# ANSI slots follow the host terminal's light/dark palette automatically.
# No hardcoded RGB values, polling, external prompt framework or special font.

autoload -Uz add-zsh-hook
setopt prompt_percent
unsetopt prompt_subst

_morelkai_precmd() {
  local -i last_status=$?
  local branch dirty context='' indicator='%F{10}'
  local git_segment='' environment_segment=''

  if (( ${+commands[git]} )); then
    branch=$(command git symbolic-ref --quiet --short HEAD 2>/dev/null) ||
      branch=$(command git rev-parse --short HEAD 2>/dev/null) || branch=''
    if [[ -n $branch ]]; then
      # Escape prompt syntax from branch names; prompt_subst stays disabled.
      branch=${branch//\%/%%}
      dirty=$(command git status --porcelain --untracked-files=normal 2>/dev/null)
      git_segment=" %F{13}${branch}%f"
      [[ -n $dirty ]] && git_segment+=' %F{11}*%f'
    fi
  fi

  if [[ -n ${VIRTUAL_ENV:-} ]]; then
    context=${VIRTUAL_ENV:t}
  elif [[ -n ${CONDA_DEFAULT_ENV:-} ]]; then
    context=$CONDA_DEFAULT_ENV
  fi
  [[ -n $context ]] && environment_segment=" %F{11}(${context//\%/%%})%f"

  (( last_status )) && indicator="%F{9}${last_status} "
  PROMPT="%F{13}%n%f@%F{8}%m%f %F{14}%~%f${git_segment}${environment_segment}"$'\n'"${indicator}%#%f "
  RPROMPT=''
}

# Re-sourcing the theme must not duplicate the hook.
add-zsh-hook -d precmd _morelkai_precmd
add-zsh-hook precmd _morelkai_precmd
_morelkai_precmd
