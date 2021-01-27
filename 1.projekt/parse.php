<?php

 if ($argc == 2) {
            if ($argv[1] == "--help") {
                help();
                exit(10);
            }
            else{
                exit(10);
            }
        }


$stdin = fopen('php://stdin', 'r');             // opening file
$xml = new DomDocument('1.0' , "UTF-8");        // mandatory head
$xml->formatOutput=true;                        // formating




// ------------------------->>>>> START PARSER <<<<------------------------------------

$inst_count = 0;                                // variable for counting instructions set to 1;
$lines_count = 0;                               // variable for counting lines set to 0
$comment_count = 0;                             // variable for counting comments -> extension
$HEAD =0;                                       // variable which takes first line from standart input


    while(!feof($stdin)) {                                  // while condition if file is not at the end continue...



        $current_line = fgets($stdin);                          // variable which takes first line from standart input
        $current_line = trim($current_line);
        // -------------------->   IPPcode18 <----------------------------

        // comments counting
        if(preg_match("/^.*#.*$/", $current_line, $arrayPattern))       // R.E. for comments
            $comment_count++;


        $current_line= preg_replace("/#.*$/", "  ", $current_line);






            if((($inst_count == 0 ) && ($HEAD == 0))&&((preg_match('/^s*\.(IPPcode18)/i', $current_line , $arrayPattern)))){
                  $program = $xml->createElement("program");                  // create element program
                  $xml->appendChild($program);
                  $program->setAttribute("language" ,"IPPcode18");       // setting atributes for program
                  $HEAD = 1 ;

            }

            else if(($inst_count > 0 ) &&  ($HEAD != 1)){
                // Lexical Error: Missing Head
                exit(21) ;
            }



        // -------------------->   MOVE <var> <symb> <-----------------------------------   //
        // -------------------->  INT2CHAR <var> <symb>  <--------------------------------  //
        // -------------------->  NOT <var> <symb> <-----------------------------------     //
        // ------------------------>  STRLEN <var> <symb>  <--------------------------------//
        // ------------------------>  TYPE <var> <symb>   <-------------------------------- //

        /*

        REGEX for MOVE|INT2CHAR|NOT|STRLEN|TYPE works = line can have any number of whitespaces form start after whitespace it must be keyword MOVE,INT2CHAR,NOT,STRLEN,TYPE after keyword follows 1-more whitespaces then there are groups for <var> and <symb> where can not be # and also " " between this two groups can be 1-more whitespaces and at the end after this groups is space for 0-inf whitspaces with ending string char $.For all regex is basically prescription the same so i will describe only some changes...eventually there is char i which means that user can input keyword in any type of cases..f.e. moVe will be valid etc.

        */
       else  if(preg_match('/^\s*(MOVE|INT2CHAR|NOT|STRLEN|TYPE)\s+([^# ]+)\s+([^# ]+)\s*$/i',$current_line , $arrayPattern)){
           if ($HEAD == 0){ exit(21);}
           $var_value = isVariable($arrayPattern[2]);                      // controlling if written word is correct variable f.e. LF@name

           $type = decideSymbType($arrayPattern[3]);                       // controoling if written word is correct variable or constant |return TYPE|
           $value = decideSymbValue($arrayPattern[3]);                     // controoling if written word is correct variable or constant |return VALUE|

           $instruction = $xml->createElement("instruction");                  // creating element instruction
           $program->appendChild($instruction);                                      // instruction is child of program
           $instruction->setAttribute("order" , $inst_count);                  // setting argument of order with instruction_counter starts with = 1
           $instruction->setAttribute("opcode", strtoupper($arrayPattern[1])); // setting argument of opcode with value of KEYWORD always written in uppercase
           $argv1 = $xml->createElement("arg1" ,  $var_value);          // creating argv1 element with value of variable
           $instruction->appendChild($argv1);                                        // argv1 element is child of instruction element
           $argv1->setAttribute("type","var");                            // setting argument of argv1...
           $argv2 = $xml->createElement("arg2", $value);                      // creating element argv2
           $instruction->appendChild($argv2);                                        // argv2 element is child of instruction element
           $argv2->setAttribute("type",$type);                                 // setting argument of argv2....


        }

        // --------------------> CREATE_FRAME <--------------------------------
        // -------------------->  RETURN <----------------------------------
        // --------------------> PUSHFRAME <--------------------------------
        // --------------------> POPFRAME <--------------------------------
        // ------------------------>  BREAK <--------------------------------

        /*

        REGEX for CREATEFRAME|PUSHFRAME|POPFRAME|RETURN works = line can have any number of whitespaces from start after whitespace it must be keyword CREATEFRAME|PUSHFRAME|POPFRAME|RETURN after keyword follows 1-more whitespaces then there are no groups

        */

        else if(preg_match('/^\s*(CREATEFRAME|PUSHFRAME|POPFRAME|RETURN|BREAK)\s*$/i' , $current_line , $arrayPattern)){
            if ($HEAD == 0){ exit(21);}
            $instruction = $xml->createElement("instruction");                      // creating element instruction
            $program->appendChild($instruction);                                          // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                      // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));    // setting argument of opcode with value of KEYWORD always written in uppercase
        }

        /*

        REGEX for DEFVAR|POPS works = line can have any number of whitespaces from start after whitespace it must be keyword DEFVAR|POPS after keyword follows 1-more whitespaces then there is 1 group <var> where can not be # and also " "...

        */

        // -------------------->  DEFVAR <var> <--------------------------------
        // -------------------->  POPS <var> <--------------------------------

        else if(preg_match('/^\s*(DEFVAR|POPS)\s*([^# ]+)\s*$/i' , $current_line , $arrayPattern)){
            if ($HEAD == 0){ exit(21);}
            $var_value = isVariable($arrayPattern[2]);                                    // controlling if written word is correct variable f.e. LF@name

            $instruction = $xml->createElement("instruction");                      // creating element instruction
            $program->appendChild($instruction);                                          // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                      // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));    // setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $var_value);              // creating argv1 element
            $instruction->appendChild($argv1);                                            // argv1 element is child of instruction element
            $argv1->setAttribute("type","var");                                // setting atrubute of argv1...
        }


         /*

        REGEX for CALL|LABE|JUMP works = line can have any number of whitespaces from start after whitespace it must be keyword CALL|LABE|JUMP after keyword follows 1-more whitespaces then there is 1 group <var> where can not be # and also " "...

        */

        // --------------------------->  CALL <label>  <--------------------------------
        // --------------------------->  LABEL <label> <--------------------------------
        // --------------------------->  JUMP <label>  <--------------------------------


        else if(preg_match('/^\s*(CALL|LABEL|JUMP)\s*([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $label_value = isLabel($arrayPattern[2]);                           // controlling if written word is correct label f.e. while is correct | 0while is incorrect

            $instruction = $xml->createElement("instruction");                          // creating instuction element
            $program->appendChild($instruction);                                              // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                          // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));        // setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $label_value);                  // creating argv1 element
            $instruction->appendChild($argv1);                                                // argv1 is child of instruction
            $argv1->setAttribute("type","label");                                  // setting atrribute for argv1
        }

        /*

        REGEX for PUSHS|WRITE|DPRINT|WRITE works same as other.... but they have group <symb>....in other words i describe concrete example on previous regexes.....they are basically same..

        */

        // -------------------->  PUSHS <symb> <--------------------------------
        // -------------------->  WRITE <symb> <--------------------------------
        // -------------------->  DPRINT <symb><--------------------------------

        else if(preg_match('/^\s*(PUSHS|DPRINT|WRITE)\s*([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $type = decideSymbType($arrayPattern[2]);                           // controlling if written word is correct variable or constant |return TYPE|
            $value = decideSymbValue($arrayPattern[2]);                         // controlling if written word is correct variable or constant |return VALUE|

            $instruction = $xml->createElement("instruction");                  // creating instruction element
            $program->appendChild($instruction);                                      // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                  // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode", strtoupper($arrayPattern[1])); // setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $value);                    // creating argv1 element
            $instruction->appendChild($argv1);                                        // argv1 is child of instruction element
            $argv1->setAttribute("type",$type);                                 // setting atrribute for argv1

        }
        /*

        REGEX for ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT works same as other.... but they have groups <var> <symb1> <symb2>

        */

        // -------------------->  ADD <var> <symb1> <symb2> <--------------------------------
        // -------------------->  SUB <var> <symb1> <symb2> <--------------------------------
        // -------------------->  MUL <var> <symb1> <symb2> <--------------------------------
        // -------------------->  IDIV <var> <symb1> <symb2> <--------------------------------
        // -------------------->  LT <var> <symb1> <symb2> <--------------------------------
        // -------------------->  GT <var> <symb1> <symb2> <--------------------------------
        // -------------------->  EQ <var> <symb1> <symb2> <--------------------------------
        // -------------------->  AND <var> <symb1> <symb2> <--------------------------------
        // -------------------->  OR <var> <symb1> <symb2> <--------------------------------
        // -------------------->  STRI2INT <var> <symb1> <symb2>  <--------------------------------

        else if(preg_match('/^\s*(ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT)\s+([^# ]+)\s+([^# ]+)\s+([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $var_value = isVariable($arrayPattern[2]);                                       // controlling if written word is correct variable f.e. LF@name
            $type1 = decideSymbType($arrayPattern[3]);                          // controlling if written word is correct variable or constant |return TYPE1|
            $type2 = decideSymbType($arrayPattern[4]);                          // controlling if written word is correct variable or constant |return TYPE2|
            $value1 = decideSymbValue($arrayPattern[3]);                        // controlling if written word is correct variable or constant |return VALUE1|
            $value2 = decideSymbValue($arrayPattern[4]);                        // controlling if written word is correct variable or constant |return VALUE2|

            $instruction = $xml->createElement("instruction");                  // creating instuction element
            $program->appendChild($instruction);                                      // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                  // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));// setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $var_value);          // creating argv1 element
            $instruction->appendChild($argv1);                                        // argv1 is child of instruction elelement
            $argv1->setAttribute("type","var");                            // setting argument argv1...
            $argv2 = $xml->createElement("arg2", $value1);                     // creating argv2 element
            $instruction->appendChild($argv2);                                        // argv2 is child of instruction elelement
            $argv2->setAttribute("type",$type1);                                // setting argument argv2...
            $argv3 = $xml->createElement("arg3", $value2);                     // creating argv3 element
            $instruction->appendChild($argv3);                                        // argv3 is child of instruction elelement
            $argv3->setAttribute("type",$type2);                                // setting argument argv3...
        }

        /*

        REGEX for READ works same as other.... but they have groups <var> <type>

        */

        // ------------------------>  READ <var> <type>  <--------------------------------

        else if(preg_match('/^\s*(READ)\s+([^# ]+)\s+([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $var_value = isVariable($arrayPattern[2]);                                        // controlling if written word is correct variable f.e. LF@name
            $type1 = isType($arrayPattern[3]);                                            // controlling if written word is correct type f.e int correct | booollleeen incorrect

            $instruction = $xml->createElement("instruction");                   // creating instuction element
            $program->appendChild($instruction);                                       // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                   // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1])); // setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $var_value);           // creating argv1 element
            $instruction->appendChild($argv1);                                         // argv1 is child of instruction elelement
            $argv1->setAttribute("type","var");                             // setting argument argv1...
            $argv2 = $xml->createElement("arg2" , $type1);           // creating argv2 element
            $instruction->appendChild($argv2);                                         // argv2 is child of instruction elelement
            $argv2->setAttribute("type", "type");                                // setting argument argv2...
        }

        /*

        REGEX for CONCAT|GETCHAR|SETCHAR works same as other.... but they have groups <var> <symb1> <sym2>

        */

        // ------------------------>  CONCAT <var> <symb1> <sym2> <--------------------------------
        // ------------------------>  GETCHAR <var> <symb1> <symb2>  <--------------------------------
        // ------------------------>  SETCHAR <var> <symb1> <symb2>  <--------------------------------

        else if(preg_match('/^\s*(CONCAT|GETCHAR|SETCHAR)\s+([^# ]+)\s+([^# ]+)\s+([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $var_value = isVariable($arrayPattern[2]);                          // controlling if written word is correct variable f.e. LF@name
            $type1 = decideSymbType($arrayPattern[3]);                          // controlling if written word is correct variable or constant |return TYPE1|
            $type2 = decideSymbType($arrayPattern[4]);                          // controlling if written word is correct variable or constant |return TYPE2|
            $value1 = decideSymbValue($arrayPattern[3]);                        // controlling if written word is correct variable or constant |return VALUE1|
            $value2 = decideSymbValue($arrayPattern[4]);                        // controlling if written word is correct variable or constant |return VALUE2|

            $instruction = $xml->createElement("instruction");                  // creating instuction element
            $program->appendChild($instruction);                                      // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                  // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));// setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" ,  $var_value);          // creating argv1 element
            $instruction->appendChild($argv1);                                        // argv1 is child of instruction elelement
            $argv1->setAttribute("type","var");                            // setting argument argv1...
            $argv2 = $xml->createElement("arg2", $value1);                     // creating argv2 element
            $instruction->appendChild($argv2);                                        // argv2 is child of instruction elelement
            $argv2->setAttribute("type",$type1);                                // setting argument argv2...
            $argv3 = $xml->createElement("arg3",  $value2);                    // creating argv3 element
            $instruction->appendChild($argv3);                                        // argv3 is child of instruction elelement
            $argv3->setAttribute("type",$type2);                                // setting argument argv3...
        }

        /*

        REGEX for JUMPIFEQ|JUMPIFNEQ works same as other.... but they have groups <label> <symb1> <symb2>

        */

        // ---------------------------->  JUMPIFEQ <label> <symb1> <symb2> <--------------------------------
        // ---------------------------->  JUMPIFNEQ <label> <symb1> <symb2> <--------------------------------


        else if(preg_match('/^\s*(JUMPIFEQ|JUMPIFNEQ)\s+([^# ]+)\s+([^# ]+)\s+([^# ]+)\s*$/i' , $current_line , $arrayPattern)) {
            if ($HEAD == 0){ exit(21);}
            $label_value = isLabel($arrayPattern[2]);                                          // controlling if written word is correct label f.e. while is correct | 0while is incorrect
            $type1 = decideSymbType($arrayPattern[3]);                          // controlling if written word is correct variable or constant |return TYPE1|
            $type2 = decideSymbType($arrayPattern[4]);                          // controlling if written word is correct variable or constant |return TYPE2|
            $value1 = decideSymbValue($arrayPattern[3]);                        // controlling if written word is correct variable or constant |return VALUE1|
            $value2 = decideSymbValue($arrayPattern[4]);                        // controlling if written word is correct variable or constant |return VALUE2|

            $instruction = $xml->createElement("instruction");                  // creating instuction element
            $program->appendChild($instruction);                                // instruction is child of program
            $instruction->setAttribute("order" , $inst_count);                  // setting argument of order with instruction_counter starts with = 1
            $instruction->setAttribute("opcode",  strtoupper($arrayPattern[1]));// setting argument of opcode with value of KEYWORD always written in uppercase
            $argv1 = $xml->createElement("arg1" , $label_value);          // creating argv1 element
            $instruction->appendChild($argv1);                                  // argv1 is child of instruction elelement
            $argv1->setAttribute("type","label");                               // setting argument argv1...
            $argv2 = $xml->createElement("arg2", $value1);                     // creating argv2 element
            $instruction->appendChild($argv2);                                  // argv2 is child of instruction elelement
            $argv2->setAttribute("type",$type1);                                // setting argument argv2...
            $argv3 = $xml->createElement("arg3",  $value2);                    // creating argv3 element
            $instruction->appendChild($argv3);                                  // argv3 is child of instruction elelement
            $argv3->setAttribute("type",$type2);                                // setting argument argv3...


        }
        // free line without chars
        elseif(preg_match('/^\s*$/',$current_line)) {
            $inst_count--;
        }
        // comment at the start of the program
        else if(preg_match('/^(\s*|(#.*))$/i',$current_line)){
            $inst_count--;
        }
        else {
                // exiting with value 21 -> Lexical
                exit(21);   // no match of any regex so LEX error...
        }

    $inst_count++;
    $lines_count++;
            // ------------------------->>>>> END PARSER <<<<------------------------------------
    }


    $inst_count--;

    if ((parseArgumets($argc , $argv , $comment_count , $inst_count)) == 10){        // PARSING ARGUMENTS
        exit(10);
    };

    if ($HEAD == 0){
        exit(21);
    }
    echo $xml->saveXML();
    fclose($stdin);

    exit(0);

    //-----------------------> <var>  <-----------------------------

    /**
     * @brief function which takes <var> group and evaluate it
     * @param $current_line
     * @return string
     */
    function isVariable ($arrayPattern){

        // The XML specification defines four "predefined entities" representing special characters, and requires that all XML processors honor them.
        $pom = preg_replace("/&/", "&amp;", $arrayPattern);
        $pom = preg_replace("/>/", "&gt;", $pom);
        $pom = preg_replace("/</", "&lt;", $pom);
        $arrayPattern = $pom;
        // match variable
        if (preg_match('/^\s*(LF|GF|TF)@[a-zA-Z%$&*_-][a-zA-Z]*/', $arrayPattern)){
            return $arrayPattern;
        }
        else{
            // exiting with value 21 -> Lexical
            exit(21);
        }
    }
    // ---------------------> DECIDE SYMB TYPE <-------------------------------

    /**
     * @brief Fucntion which take <symb> group and then returns value of it
     * @param $arrayPattern
     * @return mixed
     */
    function decideSymbType($arrayPattern){
        // The XML specification defines four "predefined entities" representing special characters, and requires that all XML processors honor them.
        $pom = preg_replace("/&/", "&amp;", $arrayPattern);
        $pom = preg_replace("/>/", "&gt;", $pom);
        $pom = preg_replace("/</", "&lt;", $pom);
        $arrayPattern = $pom;
        if(preg_match('/^\s*(LF|GF|TF)@[a-zA-Z%$&*_-][a-zA-Z]*/' , $arrayPattern , $subArrayPatter)){
            return $subArrayPatter[1] = "var";
        }
        else {
            if(preg_match('/^s*(string)@([^#\\_][0-9\\a-zA-Z%$\&;\$*_-]*)/', $arrayPattern , $subArrayPatter)){     // --> povinne na zaciatku string@ , po @ sa moze vystkytovac vsetko okrem #_\
                $arrayOfChars = $subArrayPatter[2];// it is array after string@...... this dots i get so f.e. -> /005thisisstring/222
                for ($i = 0; $i < (strlen($arrayOfChars))-1; $i++) {
                    if($arrayOfChars[$i] == "\\"){
                        if((($arrayOfChars[$i+1]) > '-1')  && (($arrayOfChars[$i+1]) < '10') && (($arrayOfChars[$i+2]) > '-1')  && (($arrayOfChars[$i+2]) < '10') && (($arrayOfChars[$i+3]) > '-1')  && (($arrayOfChars[$i+3]) < '10')){
                            // char was found... ) we can continue f.e. /201
                        }
                        else{
                            // exiting with value 21 -> Lexical
                            exit(21);
                        }
                    }
                }
            }
            // match integer
            else if(preg_match('/^\s*(int)@([-|+]?[0-9]+(\s*|(#.*)))\s*$/' , $arrayPattern , $subArrayPatter)){
            }
            // match boolean
            else if (preg_match('/^\s*(bool)@(true|false)\s*/' , $arrayPattern , $subArrayPatter)){          // checking bool type... it can be bool@false bool@true bool@
            }
            // match string
            else if(preg_match('/^s*(string)@()/', $arrayPattern , $subArrayPatter)){
            }
            else {

                // exiting with value 21 -> Lexical
                exit(21);
            }
            return $subArrayPatter[1];
        }
    }

    // ---------------------> DECIDE SYMB VALUE <-------------------------------

    /**
     * @brief Fucntion which take <symb> group and then returns value of it
     * @param $arrayPattern
     * @return mixed
     */
    function decideSymbValue($arrayPattern){
        // The XML specification defines four "predefined entities" representing special characters, and requires that all XML processors honor them.
        $pom = preg_replace("/&/", "&amp;", $arrayPattern);
        $pom = preg_replace("/>/", "&gt;", $pom);
        $pom = preg_replace("/</", "&lt;", $pom);
        $arrayPattern = $pom;

        // SYMB -> VAR
        if(preg_match('/^\s*(LF|GF|TF)@[a-zA-Z%$&*_-][a-zA-Z]*/' , $arrayPattern , $subArrayPatter)){
            return $subArrayPatter[0];                      // return whole LF@ahoj
        }
        else{
        // SYMB -> CONST]
             // match string
            if(preg_match('/^s*(string)@([^#\\_][0-9\\a-zA-Z%$\&;*_-]*\s*)$/', $arrayPattern , $subArrayPatter)){     // --> povinne na zaciatku string@ , po @ sa moze vystkytovac vsetko okrem #_\
                $arrayOfChars = $subArrayPatter[2];// it is array after string@...... this dots i get so f.e. -> /005thisisstring/222
                for ($i = 0; $i < (strlen($arrayOfChars))-1; $i++) {
                    if($arrayOfChars[$i] == "\\"){
                        if((($arrayOfChars[$i+1]) > '-1')  && (($arrayOfChars[$i+1]) < '10') && (($arrayOfChars[$i+2]) > '-1')  && (($arrayOfChars[$i+2]) < '10') && (($arrayOfChars[$i+3]) > '-1')  && (($arrayOfChars[$i+3]) < '10')){
                           // char was found... ) we can continue f.e. /201
                        }
                        else{
                            // exiting with value 21 -> Lexical
                            exit(21);
                        }
                    }
                }
            }
            else if (preg_match('/^\s*(LF|GF|TF)@([a-zA-Z%$&*_-][a-zA-Z])*$/', $arrayPattern , $subArrayPatter)){
            }
            // match integer
            else if(preg_match('/^\s*(int)@([-|+]?[0-9]+(\s*|(#.*)))$/' , $arrayPattern , $subArrayPatter)){
            }
            // match boolean
            else if (preg_match('/^\s*(bool)@(true|false)$/' , $arrayPattern , $subArrayPatter)){          // checking bool type... it can be bool@false bool@true bool@
            }
            // match string
            else if(preg_match('/^s*(string)@()/', $arrayPattern , $subArrayPatter)){
            }
            else {
                // exiting with value 21 -> Lexical
                exit(21);

            }

            return $subArrayPatter[2];
        }
    }

    // -------------------> <label> <------------------------
    /**
     * @brief Function which takes <label> group and evaluate it
     * @param $current_line
     */

    function isLabel ($arrayPattern){
        // The XML specification defines four "predefined entities" representing special characters, and requires that all XML processors honor them.
        $temp_array = $arrayPattern;


        if(preg_match('/\;/', $temp_array)){                    // if there will be ; then exit else
            // exiting with value 21 -> Lexical
            exit(21);
        }

        $pom = preg_replace("/&/", "&amp;", $arrayPattern );
        $pom = preg_replace("/>/", "&gt;", $pom);
        $pom = preg_replace("/</", "&lt;", $pom);
        $arrayPattern  = $pom;


        // match label
        if(preg_match('/^\s*[a-z_&$%-*A-Z][a-z\-\_\;\$\&\%\*A-Z0-9]*\s*$/',$arrayPattern , $subArrayPattern)){

            return $subArrayPattern[0];
        }
        else{
            // exiting with value 21 -> Lexical
            exit(21);
        }

    }

    /**
     * @brief Function which take type group and evaluate request
     * @param $current_line
     */

    function isType($arrayPattern){

        // match string
        if(preg_match('/^\s*(string)(\s*|(#.*))$/', $arrayPattern ,$subArrayPatter )){
            return $subArrayPatter[1];
        }
        // match integer
        else if(preg_match('/^\s*(int)(\s*|(#.*))$/' , $arrayPattern , $subArrayPatter)){
            return $subArrayPatter[1];
        }
        // match boolean
        else if (preg_match('/^\s*(bool)(\s*|(#.*))$/' , $arrayPattern ,  $subArrayPatter)){
            return $subArrayPatter[1];
        }
        else {
            // exiting with value 21 -> Lexical
            exit (21);
        }

    }

    /**
     * @bief Function which print help to user
     */

    function help(){
        echo (
            "\t\t---> Usage: ".
            "parser.php [options] <---\n".
            "[*******************************************************************************]\n".
            "[\tOptions:\t\t\t\t\t\t\t\t]\n".
            "[\t\t--help            will show help\t\t\t\t]\n".
            "[\t\t--stats=file.txt --comments --loc\t\t\t\t]\n".
            "[\t\t--stats=file.txt --comments\t\t\t\t\t]\n".
            "[\t\t--stats=file.txt --loc\t\t\t\t\t\t]\n".
            "[\t       YOU CAN DO IT IN ANY ORDER\t\t\t\t\t]\n".
            "[\tExample:\t\t\t\t\t\t\t\t]\n".
            "[\t\tphp5.6 parse.php --help \t\t\t\t\t]\n".
            "[\t\tphp5.6 parse.php --stats=file.txt --comments -loc < test.txt \t]\n".
            "[\t\tphp5.6 parse.php --stats=file.txt --comments < test.txt \t]\n".
            "[\t\tphp5.6 parse.php --stats=file.txt --loc < test.txt \t\t]\n".
            "[\t\tphp5.6 parse.php < test.txt \t\t\t\t\t]\n".
            "[*******************************************************************************]\n"
        );

    }

    /**
     * @brief Function which parsing arguments
     * @param $argc
     * @param $argv
     * @param $comment_count
     * @param $inst_count
     */
    function parseArgumets($argc , $argv ,   $comment_count , $inst_count)
    {
        if ($argc == 2) {
            if ($argv[1] == "--help") {
                help();
                exit(10);
            }
            else{
                exit(10);
            }
        }
        else if ($argc == 4){

            if((preg_match('/^(--stats=)(.*)$/' , $argv[1] , $arr)) || ((preg_match('/(^--stats=)(.*)$/' , $argv[2] , $arr))) || ((preg_match('/(^--stats=)(.*)$/' ,  $argv[3], $arr)))) {   //  in the arr[1] will be path of the file
                $file = fopen($arr[2], "w");                 // if there will be another
                if(!$file){                                        // if $file == False exiting by 11 value no permission to write to file
                    exit(12);
                }
                if(((preg_match('/^(--loc)$/' , $argv[1])) || ((preg_match('/^(--loc)$/' , $argv[2]))) || ((preg_match('/^(--loc)$/' , $argv[3])))) &&  ((preg_match('/^(--comments)$/' , $argv[1])) || ((preg_match('/^(--comments)$/' , $argv[2]))) ||  (preg_match('/^(--comments)$/' , $argv[3])))){
                    if($argv[1] == "--loc" && ($argv[2] != "--comments" || $argv[3] != "--comments")){
                        fwrite($file, $inst_count . "\n");
                        if($argv[2] == "--comments"){
                            fwrite($file , $comment_count . "\n");
                            return 0;
                        }
                        else if($argv[3] == "--comments"){
                            fwrite($file , $comment_count . "\n");
                            return 0;
                        }
                    }
                    else if(($argv[1] == "--comments") && ($argv[2] != "--loc" || $argv[3] != "--loc")){
                         fwrite($file, $comment_count . "\n");
                        if($argv[2] == "--loc"){
                              fwrite($file , $inst_count . "\n");
                            return 0;
                        }
                        else if($argv[3] == "--loc"){
                              fwrite($file , $inst_count . "\n");
                            return 0;
                        }
                    }
                    else if(($argv[2] == "--loc") && ($argv[3] == "--comments")){
                        fwrite($file , $inst_count . "\n");
                        fwrite($file , $comment_count . "\n");
                        return 0;
                    }
                    else if(($argv[2] == "--comments") && ($argv[3] == "--loc")){
                        fwrite($file, $comment_count . "\n");
                        fwrite($file , $inst_count . "\n");
                        return 0;
                    }

                }
                else{
                    fclose($file);
                    exit(10);

                }
            }
            else{
                exit(10);
            }
        }
        else if ($argc == 3){
            if((preg_match('/^(--stats=)(.*)$/' , $argv[1], $arr)) || (preg_match('/(^--stats=)(.*)$/' , $argv[2], $arr))) {   //  in the arr[2] will be path of the file
                $file = fopen($arr[2], "w");                 // if there will be another
                if(!$file){                                        // if $file == False exiting by 11 value no permission to write to file
                    exit(12);
                }
                if(((preg_match('/^(--loc)$/' , $argv[1])) || (preg_match('/^(--loc)$/' , $argv[2]))) ||  ((preg_match('/^(--comments)$/' , $argv[1])) || (preg_match('/^(--comments)$/' , $argv[2])))){
                    if($argv[1] == "--loc") {
                         fwrite($file, $inst_count);
                        return 0;
                    }
                    else if($argv[1] == "--comments"){
                          fwrite($file , $comment_count);
                        return 0;
                    }
                    else if($argv[2] == "--comments"){
                          fwrite($file , $comment_count);
                        return 0;
                    }
                    else if($argv[2] == "--loc"){
                          fwrite($file , $inst_count);
                        return 0;
                    }
                }
                else{
                    fclose($file);
                    exit(10);
                }
            }
            else{
                exit(10);
            }
        }
        else if (($argc != 1) && ($argc != 2) && ($argc != 3) && ($argc != 4)) {
            exit(10);
        }

    }
?>