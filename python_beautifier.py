class Beautifier:
    def __init__(self):
        global parser_pos
        parser_pos = 0

        # data will be stored here before it is concatenated to the output
        # string.
        # dummy empty strings so that certain index calls don't return out of
        # bounds
        self.data = ['', '']
        self.token_type_list = ['', '']
        self.last_token_type = ''
        self.last_last_token_type = ''
        self.last_last_last_token_type = ''
        self.last_last_last_last_token_type = ''

        self.input = ''
        self.paren_nested_level = 0
        self.paren_type = {0: ''}
        self.open_paren_index = {0: 0}
        self.chars_since_new_line = 0
        self.line_indent_level = -1

        # Enable/disable/adjust functionality
        self.wrap_comments = True
        self.wrap_inside_parens = True
        self.add_parens_to_keywords_with_colons = True
        self.newlines_to_keep = 2
        # find a way to set this to be the sublime configured num of spaces in
        # a tab
        self.tab_spaces = 4
        self.line_limit = 80

        self.punctuation = (',')
        self.operators = ('!=', '%', '&', '*', '**', '+', '+=', '-=', '-', '/',
                          '//', '<', '<<', '<=', '~', '==', '=', '>', '>=', '>>',
                          '^', '|', '<>', '*=', '/=', '%=', '**=', '//=', '|=',
                          '&=', '^=')
        # operators that should maybe or maybe not be followed by " "
        self.operators_unary = ('+', '-', '~', '*', '**')
        self.operators_maybe_pre_space = ('+', '-', '--', '++', '~')
        self.spacing_tokens = ('TK_NEW_LINE', 'TK_CARRIAGE_RETURN',
                               'TK_WHITE_SPACE')
        self.spacing_characters = (' ', '\t', '\r', '\n')
        self.newline_characters = ('\n', '\r')
        self.white_space_characters = (' ', '\t')
        self.open_characters = ('(', '[', '{')
        self.close_characters = (')', ']', '}')
        self.string_literal_characters = ("'", '"')
        self.keywords = ('and', 'assert', 'break', 'class', 'continue', 'def',
                         'del', 'elif', 'else', 'except', 'exec', 'finally',
                         'for', 'from', 'global', 'if', 'import', 'in', 'is',
                         'lambda', 'not', 'or', 'pass', 'print', 'raise',
                         'return', 'try', 'while', 'yield')
        self.keywords_with_parens_and_colons = ('elif', 'if', 'while')
        self.keywords_with_colons_and_no_parens = ('class', 'def', 'else',
                                                   'except', 'finally', 'try',
                                                   'for', 'lambda')

    def beautify(self, input):
        self.input = input

        while (True):
            token_text, token_type = self.get_next_token()
            if (token_type == 'TK_EOF'):
                break

            handlers = {'TK_STRING_LITERAL': self.handle_string_literal,
                        'TK_OPERATOR': self.handle_operator, 'TK_OTHER':
                        self.handle_other, 'TK_NEW_LINE': self.handle_new_line,
                        'TK_CARRIAGE_RETURN': self.handle_carriage_return,
                        'TK_WHITE_SPACE': self.handle_white_space,
                        'TK_OPEN_PAREN': self.handle_open_paren,
                        'TK_CLOSE_PAREN': self.handle_close_paren, 'TK_COMMENT':
                        self.handle_comment, 'TK_PUNCTUATION':
                        self.handle_punctuation, 'TK_KEYWORD':
                        self.handle_keyword, 'TK_COLON': self.handle_colon}

            handlers[token_type](token_text)

        # remove leading whitespace if the beautifier added it
        first_data_char = self.data[2]
        if (not self.input.startswith(first_data_char)):
            del self.data[2]

        # remove trailing new lines at end of file
        list_range = range(0, len(self.data))
        list_range.reverse()
        for i in list_range:
            if (self.data[i] == '\n'):
                self.data.pop()
            else:
                break

        # the payload
        return ''.join(self.data)

    def get_next_token(self):
        global parser_pos

        if (parser_pos >= len(self.input)):
            return '', 'TK_EOF'

        c = self.input[parser_pos]
        parser_pos += 1

        if (c in self.string_literal_characters):
            sep = c
            esc = False
            triple_quotes = False

            if (parser_pos + 1 < len(self.input) and self.input[parser_pos] ==
                self.input[parser_pos + 1] == c):
                triple_quotes = True
                sep = sep * 3
                parser_pos += 2

            resulting_string_literal = [sep]
            can_replace_double_with_single = False
            if (sep in ('"', '"""')):
                can_replace_double_with_single = True

            if (parser_pos < len(self.input)):
                cond = True
                if (triple_quotes == False):
                    cond = esc or self.input[parser_pos] != sep
                else:
                    cond = (parser_pos + 2 < len(self.input) and self.input[
                            parser_pos:parser_pos + 3] != sep) or esc
                while (cond):
                    if (esc == False and self.input[parser_pos] == "'"):
                        can_replace_double_with_single = False
                    resulting_string_literal.append(self.input[parser_pos])
                    if (not esc):
                        esc = self.input[parser_pos] == '\\'
                    else:
                        esc = False
                    parser_pos += 1
                    if (triple_quotes == False):
                        cond = esc or self.input[parser_pos] != sep
                    else:
                        cond = (parser_pos + 2 < len(self.input) and self.input[
                                parser_pos:parser_pos + 3] != sep) or esc
                    if (parser_pos >= len(self.input)):
                        # incomplete string when end-of-file reached
                        # bail out with what has received so far
                        return ''.join(resulting_string_literal), 'TK_STRING_LITERAL'

            parser_pos += 1
            if (triple_quotes == True):
                parser_pos += 2
            if (can_replace_double_with_single == True):
                resulting_string_literal[0] = "'"
                resulting_string_literal.append("'")
                if (triple_quotes == True):
                    resulting_string_literal[0] = "'''"
                    resulting_string_literal.append("''")
            else:
                resulting_string_literal.append(sep)
            return ''.join(resulting_string_literal), 'TK_STRING_LITERAL'

        elif (c in self.open_characters):
            self.paren_nested_level += 1
            self.paren_type[self.paren_nested_level] = c
            return c, 'TK_OPEN_PAREN'

        elif (c in self.close_characters):
            self.paren_nested_level -= 1
            return c, 'TK_CLOSE_PAREN'

        elif (c in self.punctuation):
            return c, 'TK_PUNCTUATION'

        elif (c == ':'):
            return c, 'TK_COLON'

        elif (c in self.operators or c == '!'):
            operator = c
            c = self.input[parser_pos]
            while (parser_pos < len(self.input) and (operator + c) in
                   self.operators):
                operator += c
                parser_pos += 1
                c = self.input[parser_pos]
            return operator, 'TK_OPERATOR'

        elif (c in self.spacing_characters):
            if (c == ' ' or c == '\t'):
                return c, 'TK_WHITE_SPACE'
            elif (c == '\n'):
                return c, 'TK_NEW_LINE'
            else:
                return c, 'TK_CARRIAGE_RETURN'

        elif (c == '#'):
            resulting_comment = c
            # add " " after # if not present
            if (parser_pos < len(self.input) and self.input[parser_pos] not in
                self.spacing_characters):
                resulting_comment += ' '
            while (parser_pos < len(self.input) and self.input[parser_pos] not
                   in self.newline_characters):
                resulting_comment += self.input[parser_pos]
                parser_pos += 1
            return resulting_comment, 'TK_COMMENT'

        # handle the TK_OTHER case
        else:
            resulting_string = c
            while (parser_pos < len(self.input)):
                c = self.input[parser_pos]
                if (c not in ('"', "'", '!', ' ', '\t', '\r', '\n', '(', '[',
                    '{', ')', ']', '}', '#', ':') and c not in self.operators
                    and c not in self.punctuation):
                    resulting_string += c
                    parser_pos += 1
                else:
                    break
            return_token_type = 'TK_OTHER'
            if (resulting_string in self.keywords):
                return_token_type = 'TK_KEYWORD'
            return resulting_string, return_token_type

    def handle_string_literal(self, token_text):
        if (self.last_token_type == 'TK_KEYWORD'):
            self.append_token(' ', 'TK_STRING_LITERAL')
        elif (self.last_token_type == 'TK_COLON'):
            if (self.paren_type[self.paren_nested_level] == '{'):
                self.append_token(' ', 'TK_WHITE_SPACE')
        self.append_token(token_text, 'TK_STRING_LITERAL')

    def handle_punctuation(self, token_text):
        if (self.last_token_type == 'TK_WHITE_SPACE'):
            self.pop()
        self.append_token(token_text, 'TK_PUNCTUATION')
        self.append_token(' ', 'TK_WHITE_SPACE')

    def handle_operator(self, token_text):
        if (token_text in self.operators_maybe_pre_space):
            if (self.last_last_token_type == 'TK_OPEN_PAREN' and
                self.last_token_type == 'TK_WHITE_SPACE'):
                self.pop()
            elif (self.last_token_type not in self.spacing_tokens):
                self.append_token(' ', 'TK_WHITE_SPACE')
        else:
            if (self.last_token_type not in self.spacing_tokens):
                self.append_token(' ', 'TK_WHITE_SPACE')
        self.append_token(token_text, 'TK_OPERATOR')
        self.append_token(' ', 'TK_WHITE_SPACE')


    def handle_other(self, token_text):
        # The following if statement handles removing the mandatory space
        # inserted following
        # an operator if the operator is a unary operator
        # explicitly tell it when to remove " " after the operator (if present)
        # we assume that every operator will already be followed by " "
        # - OTHER
        if (self.data[len(self.data) - 2] in self.operators_unary and
            self.last_token_type == 'TK_WHITE_SPACE'):
            # (- OTHER
            if (self.last_last_last_token_type == 'TK_OPEN_PAREN'):
                self.pop()

            # + - OTHER
            elif (self.last_last_last_last_token_type == 'TK_OPERATOR' and
                  self.last_last_last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

            # return - OTHER
            elif (self.last_last_last_last_token_type == 'TK_KEYWORD' and
                  self.last_last_last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

            # def test_var_args(farg, * args):
            elif (self.last_last_last_last_token_type == 'TK_PUNCTUATION' and
                  self.last_last_last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

        elif (self.last_token_type == 'TK_KEYWORD'):
            self.append_token(' ', 'TK_WHITE_SPACE')

        elif (self.last_token_type == 'TK_COLON'):
            if (self.paren_type[self.paren_nested_level] == '{'):
                self.append_token(' ', 'TK_WHITE_SPACE')

        # don't need line continuation symbol within parens
        if (token_text == '\\' and self.paren_nested_level > 0):
            pass
        else:
            self.append_token(token_text, 'TK_OTHER')

    def handle_keyword(self, token_text):
        self.append_token(token_text, 'TK_KEYWORD')

    def handle_white_space(self, token_text):
        if (self.last_token_type in ('TK_NEW_LINE', 'TK_CARRIAGE_RETURN')):
            # we keep the previous last_token_type here because we want to
            # preserve all whitespace immediately following a new line.
            self.append_token(token_text, self.last_token_type)
        elif (self.last_token_type in ('TK_WHITE_SPACE', 'TK_OPEN_PAREN')):
            pass
        elif (self.last_token_type == 'TK_COLON' and self.paren_type[
              self.paren_nested_level] == '['):
            pass
        else:
            self.append_token(token_text, 'TK_WHITE_SPACE')

    def handle_new_line(self, token_text):
        # we let the line wrapping algorithm handle new lines if we are inside
        # any type of parens. Hence, we ignore new line symbols we read in here
        if (self.paren_nested_level > 0 and token_text != '\nFORCE' and
            self.last_token_type != 'TK_COMMENT'):
            return
        if (token_text == '\nFORCE'):
            token_text = '\n'

        # trim whitespace at end of line
        while (self.data[len(self.data) - 1] in self.white_space_characters):
            self.data.pop()

        add_line = True
        for i in range(0, self.newlines_to_keep + 1):
            if (self.data[len(self.data) - 1 - i] == '\n'):
                if (i == self.newlines_to_keep):
                    add_line = False
                    self.line_indent_level = -1
                    self.chars_since_new_line = 0
            else:
                break

        if (add_line == True):
            self.append_token(token_text, 'TK_NEW_LINE')

    def handle_carriage_return(self, token_text):
        self.append_token(token_text, 'TK_CARRIAGE_RETURN')

    def handle_open_paren(self, token_text):
        if (self.last_last_token_type not in ('TK_OPERATOR', 'TK_KEYWORD') and
            self.last_token_type == 'TK_WHITE_SPACE'):
            self.pop()
        if (self.last_token_type in ('TK_KEYWORD')):
            self.append_token(' ', 'TK_WHITE_SPACE')

        self.append_token(token_text, 'TK_OPEN_PAREN')
        self.open_paren_index[self.paren_nested_level] = self.chars_since_new_line

    def handle_close_paren(self, token_text):
        if (self.last_token_type == 'TK_WHITE_SPACE' and
            self.last_last_token_type not in self.spacing_tokens):
            self.pop()

        self.append_token(token_text, 'TK_CLOSE_PAREN')

    def handle_comment(self, token_text):
        if (self.last_token_type not in self.spacing_tokens):
            self.append_token(' ', 'TK_WHITE_SPACE')

        # wrap long comments
        if (self.chars_since_new_line + len(token_text) > self.line_limit and
            self.wrap_comments == True):
            token_text_list = list(token_text)
            new_line_range = range(0, self.line_limit -
                                   self.chars_since_new_line)
            new_line_range.reverse()
            for i in new_line_range:
                if (token_text_list[i] in self.spacing_characters):
                    self.handle_comment(''.join(token_text_list[0:i]))
                    indent_level = self.line_indent_level
                    self.handle_new_line('\n')
                    for j in range(0, indent_level):
                        self.append_token(' ', 'TK_WHITE_SPACE')
                    token_text_list.insert(i, '#')
                    self.handle_comment(''.join(token_text_list[i:]))
                    break
        else:
            self.append_token(token_text.rstrip(), 'TK_COMMENT')

    def handle_colon(self, token_text):
        # my_list[2:5]
        if (self.paren_type[self.paren_nested_level] == '['):
            if (self.last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

        # array = {'foo': 'bar'}
        elif (self.paren_type[self.paren_nested_level] == '{'):
            if (self.last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

        # colon must have been used with a keyword, e.g. "else:"
        else:
            if (self.last_token_type == 'TK_WHITE_SPACE'):
                self.pop()

            if (self.add_parens_to_keywords_with_colons == True):
                add_parens_here = True

                if (self.last_token_type != 'TK_CLOSE_PAREN'):
                    loop_range = range(0, len(self.data))
                    loop_range.reverse()
                    for i in loop_range:
                        if (self.data[i] in
                            self.keywords_with_colons_and_no_parens):
                            add_parens_here = False
                            break
                        elif (self.data[i] in
                              self.keywords_with_parens_and_colons):
                            break

                else: # ):
                    closing_paren_count = 0
                    loop_range = range(0, len(self.data) - 1)
                    loop_range.reverse()
                    for i in loop_range:
                        if (self.data[i] in
                            self.keywords_with_colons_and_no_parens):
                            add_parens_here = False
                            break
                        elif (self.data[i] in
                              self.keywords_with_parens_and_colons and
                              closing_paren_count != -1):
                            # we found a keyword before finding the matched
                            # open paren.
                            # break out to avoid doing bad things.
                            add_parens_here = False
                            break
                        elif (self.data[i] in
                              self.keywords_with_parens_and_colons and
                              closing_paren_count == -1):
                            break
                        elif (self.data[i] == ')' and closing_paren_count != -1):
                            closing_paren_count += 1
                        elif (self.data[i] == '(' and closing_paren_count != -1):
                            closing_paren_count -= 1
                            if (closing_paren_count == -1):
                                # we found the matched paren
                                if (self.data[i - 2] in
                                    self.keywords_with_parens_and_colons):
                                    add_parens_here = False
                                    break

                if (add_parens_here == True):
                    loop_range = range(0, len(self.data))
                    loop_range.reverse()
                    for i in loop_range:
                        if (self.data[i] == '\\'):
                            del self.data[i]
                        elif (self.data[i] in
                              self.keywords_with_parens_and_colons):
                            self.data.insert(i + 2, '(')
                            break
                    self.append_token(')', 'TK_CLOSE_PAREN')

        self.append_token(token_text, 'TK_COLON')


    def append_token(self, token_text, token_type):
        if (self.line_indent_level == -1 and token_type not in
            self.spacing_tokens):
            self.line_indent_level = self.chars_since_new_line

        # wrap lines if we are inside some sort of parens
        if (self.chars_since_new_line + len(token_text) > self.line_limit and
            self.paren_nested_level > 0 and self.wrap_inside_parens):
            # wrap only on these tokens
            if (token_type in ('TK_STRING_LITERAL', 'TK_OTHER', 'TK_KEYWORD')):
                self.handle_new_line('\nFORCE')
                # We wrap to align with the outter most paren block. If we were
                # instead to wrap to
                # self.open_paren_index[self.paren_nested_level] it would
                # create ugly issues in some lines
                for i in range(0, self.open_paren_index[1]):
                    self.handle_white_space(' ')

        self.data.append(token_text)
        self.token_type_list.append(token_type)
        self.last_last_last_last_token_type = self.last_last_last_token_type
        self.last_last_last_token_type = self.last_last_token_type
        self.last_last_token_type = self.last_token_type
        self.last_token_type = token_type
        if (token_text == '\t'):
            self.chars_since_new_line += self.tab_spaces
        elif (token_text in self.newline_characters):
            self.chars_since_new_line = 0
            self.line_indent_level = -1
        else:
            if (token_type == 'TK_STRING_LITERAL'):
                self.chars_since_new_line = self.get_string_literal_chars_since_new_line(
                                                                                         token_text)
            else:
                self.chars_since_new_line += len(token_text)

    def pop(self):
        last_token = self.data.pop()
        self.chars_since_new_line -= len(last_token)

    def get_string_literal_chars_since_new_line(self, token_text):
        chars_since_new_line = 0

        if (token_text.startswith("'''") or token_text.startswith('"""')):
            new_line_index = -1
            list_range = range(0, len(token_text))
            list_range.reverse()
            for i in list_range:
                if (token_text[i] == '\n'):
                    new_line_index = i
                    break

            if (new_line_index == -1):
                chars_since_new_line = self.chars_since_new_line + len(
                                                                       token_text)
            else:
                chars_since_new_line = len(token_text) - i - 1

        else:
            chars_since_new_line = self.chars_since_new_line + len(token_text)

        return chars_since_new_line


def beautify(input):
    beautifier = Beautifier()
    return beautifier.beautify(input)