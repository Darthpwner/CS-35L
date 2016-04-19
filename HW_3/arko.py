try:
            #If -w option is on and not enough line entries
    if withoutReplace and numlines > len(List_files):
                    parser.error("Must have no more than {0} lines".format(len(List_files)))
                                sys.exit()
                                        generator = randline(input_file)
                                        for index in range(numlines):
                                                        sys.stdout.write(generator.chooseline(withoutReplace))

except IOError as no_err_str:
            parser.error("I/O error({0}): {1}".
                                              format(no_err_str[0], no_err_str[1]))
