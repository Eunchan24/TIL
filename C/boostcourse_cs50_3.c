#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
void Determine_Grades(int input, int scores[], char *grades[]);
int main(void)
{
    int input = 0;
    int scores[9] = {95, 90, 85, 80, 75, 70, 65, 60, 0};
    string grades[9] = {"A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"};
    printf("학점 프로그램\n");
    printf("종료를 원하면 \"999\"를 입력\n");
    printf("[학점 테이블]\n");
    printf("점수 : ");
    for (int i = 0; i < 9 ; i++)
    {
        printf("%4i", scores[i]);
    }
    printf("\n");
    printf("학점 : ");
    for (int i = 0; i < 9 ; i++)
    {
        printf("%4s", grades[i]);
    }
    printf("\n");
    while(1)
    {
        input = get_int("성적을 입력하세요 (0 ~ 100) : ");
        if (input == 999) 
            break;
        Determine_Grades(input, scores, grades);
    }
    printf("학점 프로그램을 종료합니다.\n");
}
void Determine_Grades(int input, int scores[], string grades[])
{
    int i;
    for(i = 0; i < 9 ; i++)
    {
        if ( input > 100 || input < 0 )
        {
            printf("** %i 성적을 올바르게 입력하세요. 범위는 0 ~ 100 입니다.\n", input);
            break;
        }
        if ( input >= scores[i] )
        {
            printf("학점은 %s 입니다.\n", grades[i]);
            break;
        }
    }
}