import Text.ParserCombinators.Parsec hiding ((<|>), many)
import Control.Applicative
import Control.Monad
import Data.Set (Set, member)

data Expression = Label String
                | NotExp Expression
                | AndGroup [Expression]
                | OrGroup  [Expression]
    deriving(Show)

infixl 3 <||>
(<||>) :: Parser a -> Parser a -> Parser a
a <||> b = try a <|> b

label_abc = ['a'..'z'] ++ ['A'..'Z'] ++ ['0'..'9'] ++ "_"

expression :: Parser Expression
expression = not_exp
        <||> and_group
        <||> or_group
        <||> label_symb
label_symb :: Parser Expression
label_symb = Label <$> many1 (oneOf label_abc)

--possible whitespace
ws :: Parser String
ws = many $ char ' '

--mandatory whitepsace
ws1 :: Parser String
ws1 = many1 $ char ' '


and_symb :: Parser String
and_symb  = (ws1 *> string "and" <* ws1)
       <||> (ws  *> string  "&"  <* ws )

or_symb  :: Parser String
or_symb   = (ws1 *> string "or"  <* ws1)
       <||> (ws  *> string  "|"  <* ws )

not_symb :: Parser String
not_symb  = (ws  *> string "not" <* ws1)
       <||> (ws  *> string  "-"  <* ws )

parenthessized :: Parser a -> Parser a
parenthessized p = ws *> char '(' *> ws *> p <* ws <* char ')' <* ws

and_group :: Parser Expression
and_group = fmap AndGroup $
            parenthessized $
            expression `sepBy` and_symb

or_group :: Parser Expression
or_group = fmap OrGroup $
           parenthessized $
           expression `sepBy` or_symb

not_exp :: Parser Expression
not_exp = fmap NotExp $
    not_symb *> expression

exp_parse = label_symb <* eof
       <||> and_group <* eof
       <||> or_group <* eof
       <||> not_exp <* eof

main = do
    print $ parse exp_parse "test" "(not a or ( a))"

match :: Expression -> Set String -> Bool
match (NotExp exp) s = not $ match exp s
match (AndGroup l) s = and $ fmap (flip match s) l
match (OrGroup  l) s =  or $ fmap (flip match s) l
--match (Label lab) = member "awd"