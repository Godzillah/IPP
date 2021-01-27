<?php


/************************CONSTANTS**************************/
// PARSER RETURN VALUES
const PARSER_ARGUMENT_ERROR = 10;
const PARSER_SYN_ERR = 21;


const OK_VAL = 0;
const OK_ARG_VAL = 0;

// INTERPRET RETURN VALUES
const INTERPRET_ARGUMENT_ERROR = 10;
const INTERPRET_SYN_ERR = 21;

$GREEN = "\033[32m";
$RED = "\033[31m";
$COLOR_END = "\033[0m";

/***********************ARGUMENT PARSING********************/

$testPath = "./";                    # normal path....

if ($argc == 2) {
    if (!strcmp($argv[1], "--help") || !strcmp($argv[1], "-h")) {
        print(  "*****Test for two scripts parse.php and interpret.py.*****\n".
                "               --->  |USAGE|: [options] <---              \n".
                " [options]:                                                 \n".
                "  test.php -h | -help                                        \n".
                "  test.php -c | -clean                                        \n".
                "  test.php --directory=path                                  \n".
                "  test.php --recursive                   \n".        
                "  test.php --parse-script=file                   \n".      
                "  test.php --int-script=file                   \n".      
                 
              " [--help] [--clean]\n");
        exit(0);
    }
    else if (!strcmp($argv[1], "--clean") || !strcmp($argv[1], "-c")) {
        // Clean files
        exec('rm -f ./diff/*', $output, $ret_val);
        exec('rm -f ./out/*', $output, $ret_val);
        exit(0);
    }
    else if (preg_match('/^(--directory=)(.*)$/' , $argv[1], $arr)){
        print("You are in file...\n");
        $testPath = $arr[2];   
        print("This is path...\n" . $testPath . "\n");
        exit(0);
    }
    else if(preg_match('/^(--recursive)(.*)$/' , $argv[1])){
        print("Test are gonna find it recursive...\n");
        $testPath = $arr[2] . "/*";                                  # for recursive subfolders...
        exit(0);
    }
    else if(preg_match('/^(--parse-script=)(.*)$/' , $argv[1], $arr)){
        print("Parse file script...\n");
        $parsePath = $arr[2];   
        print("This is path...\n" . $parsePath . "\n"); 
        exit(0);
    }
    else if(preg_match('/^(--int-script=)(.*)$/' , $argv[1], $arr)){
        print("Parse file script...\n");
         $interpretPath = $arr[2];   
        print("This is path...\n" . $interpretPath . "\n"); 
        exit(0);
    }
    else {
        print("Invalid arguments. Type --help !\n");
        exit(1);
    }

}
else if ($argc != 1) {
    print("Invalid arguments. Type --help !\n");
    exit(1);
}

