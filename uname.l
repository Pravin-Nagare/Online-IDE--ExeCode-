%{
	#include<stdio.h>
	int state=0;
%}

%%
[\t \n]
"<login>"		state=1;
[a-zA-Z0-9]+|\-	{
				if(state==1)
					printf("%s",yytext);
				}
"</login>"		state=0;
.		;
%%

int yywrap()
{
	return 1;
}

main(int argc,char * argv[])
{
	FILE *in=fopen(argv[1],"r");
	yyin=in;
	yylex();
	fclose(in);
	return 0;
}
