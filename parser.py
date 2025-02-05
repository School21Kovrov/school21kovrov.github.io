import pandas as pd

def get_schedule(class_name, file_path='30.01.25.xlsx'):
    df = pd.read_excel(file_path, header=None)
    
    schedule = []
    
    class_row = 1 
    class_col = None
    
    for col in range(3, len(df.columns)): 
        if str(df.iloc[class_row, col]) == class_name:
            class_col = col
            break
    
    if class_col is None:
        return []
    
    for row in range(2, len(df)):
        lesson_number = df.iloc[row, 1]
        if pd.isna(lesson_number):
            continue
            
        time = df.iloc[row, 2]
        lesson_info = df.iloc[row, class_col]
        
        classroom = df.iloc[row + 1, class_col]

        if pd.isna(lesson_info):
            continue
            
        if pd.isna(classroom):
            classroom = ""
        temp = []
        temp.append(int(lesson_number))
        temp.append(time)
        temp.append(lesson_info)
        temp.append(classroom)
        schedule.append(temp)


    return schedule

print(get_schedule('9Г'))

