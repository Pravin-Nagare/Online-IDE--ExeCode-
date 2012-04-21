%{
	#include<stdio.h>
	#include<string.h>
	int isFound=0;
	char *uname,*me;
%}

%%
"\"name\":\""	isFound=1;
[a-zA-Z0-9\-]+	{
					if(isFound)
					{
						char temp[512];
						printf("%s\n",uname);
						printf("Project :%s",yytext);
						sprintf(temp,"git clone git://github.com/%s/%s.git /home/%s/%s/Private/%s.git" 							,uname,yytext,me,uname,yytext);
						printf("%s",temp);
						system(temp);
					}
					else
						;
				}
"\","			{
					if(isFound)
						isFound=0;
					else
						;
				}		
[.\,\:\/\_\]\}\[\{\"\- ]			;
%%
yywrap()
{
	return 1;
}

main(int argc,char * argv[])
{
	FILE *in;
	uname=(char*)malloc((strlen(argv[1])+1)*sizeof(char));
	me=(char*)malloc((strlen(argv[2])+1)*sizeof(char));
	strcpy(uname,argv[1]);
	strcpy(me,argv[2]);
//	strcat(uname,"\0");
	in=fopen("repo.txt","r");
	yyin=in;
	yylex();
	fclose(in);

	return 0;
}
