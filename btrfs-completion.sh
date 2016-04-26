_btrfs() 
{
    local cur prev 
    COMPREPLY=()
    
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    commands='subvolume filesystem balance scrub check restore inspect-internal  device send receive quota qgroup replace help version'
    commands_subvolume='snapshot delete create list find-new set-default show'
    commands_filesystem='defragment sync resize show df balance label'
    commands_device='scan add delete ready stats'
    commands_balance='start pause cancel resume status'
    commands_inspect_internal='inode-resolve logical-resolve subvolid-resolve'
    commands_scrub='start cancel resume status'
    commands_quota='enable disable rescan'
    commands_qgroup='assign remove create destroy show limit'
    commands_replace='start status cancel'

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $( compgen -W "$commands" -- "$cur" ) )
    elif [ $COMP_CWORD -eq 2 ]; then
        case $prev in
            subvolume)
                COMPREPLY=( $( compgen -W "$commands_subvolume" -- "$cur" ) )
                return 0
                ;;
            filesystem)
                COMPREPLY=( $( compgen -W "$commands_filesystem" -- "$cur" ) )
                return 0
                ;;
            device)
                COMPREPLY=( $( compgen -W "$commands_device" -- "$cur" ) )
                return 0
                ;;
            balance)
                COMPREPLY=( $( compgen -W "$commands_balance" -- "$cur" ) )
                return 0
                ;;
            scrub)
                COMPREPLY=( $( compgen -W "$commands_scrub" -- "$cur" ) )
                return 0
                ;;
            inspect-internal)
                COMPREPLY=( $( compgen -W "$commands_inspect_internal" -- "$cur" ) )
                return 0
                ;;
            quota)
                COMPREPLY=( $( compgen -W "$commands_quota" -- "$cur" ) )
                return 0
                ;;
            qgroup)
                COMPREPLY=( $( compgen -W "$commands_qgroup" -- "$cur" ) )
                return 0
                ;;
            replace)
                COMPREPLY=( $( compgen -W "$commands_replace" -- "$cur" ) )
                return 0
                ;;
        esac
    elif [ $COMP_CWORD -eq 3 ]; then
        case $prev in
            snapshot|delete|create|list|find-new|sync|df| \
            scan|add)
                _filedir -d
                return 0
                ;;
            balance)
                COMPREPLY=( $( compgen -W "$commands_balance" -- "$cur" ) )
                return 0
                ;;            
            defragment)
                _filedir
                return 0
                ;;
	    help)
                COMPREPLY=( $( compgen -W "--full" -- "$cur" ) )
                return 0
                ;;
        esac
    fi

    return 0  
}

complete -F _btrfs btrfs
