"""Provides a simple interactive CLI to start a selected build from a given set of build-configurations"""
import sys
import shlex

import build_system.build_configs as bcfg
import build_system.build_executor as bex
import build_system.build_utils as utils
import build_system.cli as cli


def run_interactive_cli():
    idx = 0
    for cfg in bcfg.configs:
        print("[" + str(idx) + "] " + cfg.get("name"))
        idx += 1
    print()  # newline

    # NOTE: argv[1] usually should be -i, therefore we need to consider this arg in all checks
    base_arg_count = 2

    if len(sys.argv) > base_arg_count:
        sel_index = int(sys.argv[base_arg_count])
    else:
        sel_index = int(input("Select a predefined build-configuration to run: "))

    print(sel_index)
    print(isinstance(sel_index, int))
    if not isinstance(sel_index, int) or sel_index < 0 or sel_index > len(bcfg.configs):
        utils.cli_exit("ERROR: Must enter a valid test index in the range [0 ... " + str(len(bcfg.configs)) + "]")

    selected_build_cfg = bcfg.configs[sel_index]

    print("Building: " + selected_build_cfg.get("name"))
    print()  # newline

    build_params = selected_build_cfg.get("params")

    # use build-steps from sys.argv or alternatively ask the user
    build_steps_argv = \
        sys.argv[base_arg_count + 1:] \
            if len(sys.argv) > base_arg_count + 1 \
            else shlex.split(input("Override build-steps ? (leave empty to run pre-configured steps): "))

    # create a parser that only expects the build-step args
    parser = cli.get_blank_parser()
    cli.init_build_steps(parser)

    # parse the build-step syntax
    user_params = parser.parse_args(build_steps_argv)

    # convert into dictionary form
    user_params = vars(user_params)

    # merge the potentially customized build-steps into the
    # original pre-defined build-config params
    # see: https://stackoverflow.com/a/15277395/425532
    build_params.update((k, v) for k, v in user_params.items() if v is not None)

    # start the build
    bex.execute_build(build_params)
