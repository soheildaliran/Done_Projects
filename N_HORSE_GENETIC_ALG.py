#class
import numpy as np
import math
import random
import time
"""
سلام
خسته نباشید
توی این سوال خواسته شده که با الگوریتم ژنتیک ماکسیمم تعداد اسب ها رو بچینین تو صفحه شطرنج
الگوریتم ژنتیک سه کلی مرحله داره
مرحله اول : initialization
توی این مرحله جمعیت اولیه درست میشن . توی این مسئله به هر فرم چینش اسب ها توی صفحه شطرنج یه عضو جمعیت میگیم
جمعیت اولیه تصادفی درست میشن به تعدادی که ما میگیم بهشون . یعنی ورودی مسئله است
بعد تا جایی که می خوایم باید دو مرحله بعدی رو اجرا کنیم
مرحله دوم : selection
یه تعدادی از افراد برتر جمعیت انتخاب میشن
مرحله سوم : generation
با اون جمعیت برتری که انتخاب کردیم توی مرحله قبل ، میایم جمعیت جدیدی درست می کنیم
یعنی اونا پدر میشن یه سری فرزند تولید میشه
اینجا من اومدم برای تولید فرزند یه تیکه از صفحه والد هاش رو می برم و به هم وصل می کنم یعنی مثلا از ستون ۰ تا ۴ اش مال یه والده
از ستون ۵ تا ۸ اش مال یه والده دیگه
توضیح ریز الگوریتم رو توی کد دادم
حواستون باشه اینا رو برای ارائه پاک کنید

توی صفحه شطرنج اگه یه خونه ۱ باشه یعنی توش اسبه اگه صفر باشه نیستش
"""


# تعداد جمعیت اولیه
population_size = 10

# احتمال جهش
p = 0.2

# این متغیر میگه از کجا باید والد ها رو ببریم و به هم وصل کنیم مثلا . همون مرحله ترکیب . این استراتژی ترکیب که گفته دلخواهه اینه در واقع
n_selection = 5

# بهترین امتیاز رو نگه داری میگنه
score = list()
score.append(0)

# بهترین جواب تا الان رو نگهداری میکنه
best_population = list()
best_population.append(np.zeros((8,8)))

record={'NoNotChanged':0,'score':0}

# لیست جمعیت رو نگهداری میکنه
population = list()

# واسه اینکه بهترین رو انتخاب کنیم باید به هر صفحه یک امتیازی بدیم
# بهش میگن fitness function
# اینجا محاسبه میشه
# به این شکل که اگه یه جا اسب بود یه نمره میگیره و اگه اسب ها هم رو تهدید کنن
# ۱۰۰ نمره منفی میگیره
def calculate_fitness(board):
    fitness = 0
    have_horse = list()
    for (x,y),value in np.ndenumerate(board) :
        if value == 1 :
            have_horse.append((x,y))
            fitness += 1

    for i in range(8):
        for j in range(8):
            if (i,j) in have_horse :
                if ((i+1,j+2) in have_horse) or ((i+1,j-2)  in have_horse) or \
                    ((i-1,j+2)  in have_horse) or ((i-1,j-2) in have_horse) or \
                    ((i + 2, j + 1)  in have_horse) or ((i -2, j +1) in have_horse) or \
                    ((i +2, j -1)  in have_horse) or ((i - 2, j - 1) in have_horse) :
                    fitness -= 100

    return fitness

# جمعیت اولیه رو رندوم تولید می کنیم
def initialize(population_size,population):

    for i in range(population_size):
        mat = np.random.random((8, 8))
        mat[mat > 0.5] = 1
        mat[mat < 0.5] = 0
        population.append({'board':mat,'score':calculate_fitness(mat)})


# برای نمایش خوشگل طور صفحه شطرنج
def printBoard(board):
    for row in range(8):
        print("", end="|")

        for col in board[row,:] :
            if col == 1:
                print("H", end="|")
            else:
                print("_", end="|")
        print("")

# این همون مرحله selection یا انتخاب هست
def selection(population) :
    sorted_population = sorted(population, key=lambda k: k['score'],reverse=True)
    printBoard(sorted_population[0]['board'])
    print(sorted_population[0]['score'])
    print('============================')
    score[0] = sorted_population[0]['score']
    best_population[0] = sorted_population[0]['board']
    updateRecord(score)
    return sorted_population[:n_selection]

# این مرحله generation یا ترکیب هست . فقط توی این مرحله علاوه بر ترکیب به احتمال p جهش هم داریم
# یعنی یه خونه ممکنه یهو ازش اسب برداریم یا اسب بذاریم توش
# به صورت تصادفی با احتمال p
def generation(population):
    new = list()
    selected = selection(population)
    for i in selected:
        for j in selected:
            new.append(\
                np.concatenate((i['board'][:,:n_selection],j['board'][:,n_selection:]),axis=1))


    for new_population in new:
        for (x, y), value in np.ndenumerate(new_population):
            if np.random.binomial(1,0.2) == 1: new_population[x,y] = abs(value - 1)

        population.append({'board':new_population,'score':calculate_fitness(new_population)})


def updateRecord(score):
    if score == record['score'] :
        record['NoNotChanged'] += 1
    else:
        record['NoNotChanged'] = 0
        record['score'] = score


# گفته انقد اجرا کنید تا پیشرفت کند بشه
# این انقد اجرا میشه تا ۲۰۰۰ تا حلقه بشه که مقدار بهتر نشده
# ممکنه دو تا سه دقیقه طول بکشه اجرا بشه
# اگه خواستین کمتر بشه ۲۰۰۰ رو کمتر کنین ولی جواب بدتری بدست میاد
while record['NoNotChanged'] < 2000 :
    initialize(population_size, population)
    generation(population)
    # time.sleep(0.2)


print("===============================")
print("===============================")
print("======== BEST SOLUTION ========")
print("===============================")
print("===============================")
print("BOARD :\n")
printBoard(best_population[0])
print("SCORE(NUMBER OF HORSES) :\n\n")
print(score[0])


