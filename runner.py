import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


class Transform_files:
    def __init__(self, period_from, period_till):
        self._period_from = period_from
        self._period_till = period_till


    def _transform(self, file, type):
        data = pd.read_csv(file, skiprows=range(0, 5), names=['Date and time', f'{type}_Value', \
            f'{type}_Min', f'{type}_Max'], delimiter=';', encoding='utf-8', decimal=",")
        data['Date and time'] = pd.to_datetime(data['Date and time'], errors='coerce', format='%d.%m.%Y %H:%M:%S')
        data = data.loc[(data['Date and time'] >= self._period_from) & (data['Date and time'] < self._period_till)]
        return data


    def __call__(self, home, *args, **kwargs):
        file_list = os.listdir(home)
        cur_C = [self._transform(f'{home}\\{i}', 'I') for i in file_list if "Сила тока фаза" in i]
        voltages = [self._transform(f'{home}\\{i}', 'U') for i in file_list if "Напряжение " in i]
        return cur_C, voltages


class Draw_graphs:
    def __init__(self, cur, voltage, obj):
        self._current = cur[0]
        self._voltages = voltage
        self._object = obj
    
    
    @staticmethod    
    def _graphic_data_for_phases(phase):
        y = phase['U_Value']
        x = x_max = x_min = phase['Date and time']
        y_max = phase['U_Max']
        y_min = phase['U_Min']
        return x, y, 'b', x_max, y_max, '--r', x_min, y_min, '--g'


    def _main(self, home, num):  
        fig = plt.figure(figsize=(16, 9))
        fig.suptitle(f'Влияние тока фазы C на фазное напряжение \n Объект РТС {self._object}\n{num}')     
        
        ax_1 = fig.add_subplot(4, 1, 1)
        ax_2 = fig.add_subplot(4, 1, 2)
        ax_3 = fig.add_subplot(4, 1, 3)
        ax_4 = fig.add_subplot(4, 1, 4)
        
        iy = self._current['I_Max']
        ix = self._current['Date and time']

        ax_1.plot(*self._graphic_data_for_phases(self._voltages[0]))
        ax_2.plot(*self._graphic_data_for_phases(self._voltages[1]))
        ax_3.plot(*self._graphic_data_for_phases(self._voltages[2]))
        ax_4.plot(ix, iy)
                
        ax_1.legend(('Среднее значение', 'Максимальное', 'Минимальное'))
        ax_1.set_ylabel('Напряжение фазы A')
        ax_2.set_ylabel('Напряжение фазы B')
        ax_3.set_ylabel('Напряжение фазы C')
        ax_4.set_ylabel('Ток фазы С\nМаксимальное значение')
        ax_4.set_xlabel('Дата и время')

        plt.savefig(f'{home}\\{num}.png', bbox_inches = 'tight', dpi = fig.dpi)
        plt.cla()
        plt.close(fig)
        
    def __call__(self, home, num, *args, **kwargs):
        self._main(home, num)
        

objects = ['Закаринье', 'Заборщина']
dates = ['10-19', '10-20', '10-21', '10-22', '10-23', '10-24', '10-25', '10-26', '10-27', \
    '10-28', '10-29', '10-30', '10-31', '11-01', '11-02', '11-03', '11-04', '11-05',  \
        '11-06', '11-07', '11-08', '11-09', '11-10', '11-11', '11-12', '11-13', '11-14', '11-15', '11-16', '11-17', '11-18']


if __name__ == '__main__':
    for obj in objects:
        home = Path('F:\Brytkov', 'Own', 'PROG', 'pars', 'analys C', f'{obj} ОСН')
        for i, md in enumerate(dates[:-1]):
            period_from = f'2022-{dates[i]} 00:00:00'
            period_till = f'2022-{dates[i+1]} 00:00:00'
            try:
                trasform = Transform_files(period_from, period_till)
                cur, volt = trasform(home)
                draw = Draw_graphs(cur, volt, obj)
                draw(home, md)
            except Exception as error:
                raise error
        


