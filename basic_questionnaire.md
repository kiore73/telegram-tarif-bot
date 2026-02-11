# Basic Questionnaire Specification

## Overview
This document specifies the "basic" questionnaire with conditional logic based on flags (anemia, nervous, skin).

## Questions

### 1. `q_gender`
*   **Text:** Укажите ваш пол
*   **Type:** single
*   **Options:** Мужчина. Женщина

### 2. `q_occupation`
*   **Text:** Ваш род занятий (можно выбрать несколько вариантов)
*   **Type:** multi
*   **Options:** Сидячая работа. Есть физическая нагрузка. Высокая умственная нагрузка / ответственность. Приходится долго стоять. Частые поездки / перелеты

### 3. `q_sport_activity`
*   **Text:** Есть ли в вашей жизни спорт или физическая активность?
*   **Type:** single
*   **Options:** Да, регулярно. Нерегулярно. Нет. Профессиональный спортсмен

### 4. `q_chronic_diseases`
*   **Text:** Есть ли у вас хронические или наследственные заболевания? Укажите.
*   **Type:** text

### 5. `q_family_diseases`
*   **Text:** Есть ли хронические или генетические заболевания у близких родственников?
*   **Type:** text

### 6. `q_surgeries`
*   **Text:** Были ли у вас операции? Какие и когда?
*   **Type:** text

### 7. `q_medications`
*   **Text:** Принимаете ли вы постоянно лекарства или БАДы? Какие?
*   **Type:** text

### 8. `q_allergy`
*   **Text:** Испытываете ли вы симптомы аллергии?
*   **Type:** single
*   **Options:** Очень часто. Иногда. Сезонно. Нет

### 9. `q_orvi`
*   **Text:** Как часто вы переносите сезонные ОРВИ?
*   **Type:** single
*   **Options:** Очень редко. 1–2 раза в год. 3–4 раза в год. Постоянно, даже летом
*   If answer == "3–4 раза в год" set flag_anemia
*   If answer == "Постоянно, даже летом" set flag_anemia

### 10. `q_daily_routine`
*   **Text:** Опишите ваш режим дня (сон, питание, работа, транспорт, прогулки).
*   **Type:** text

### 11. `q_sleep_quality`
*   **Text:** Оцените качество сна (можно несколько вариантов)
*   **Type:** multi
*   **Options:** Быстро засыпаю. Засыпаю более 40 минут. Сон крепкий без пробуждений. Сон чуткий. Есть трекер сна. Просыпаюсь легко. Просыпаюсь тяжело. Нет сил до обеда

### 12. `q_sleep_hygiene`
*   **Text:** Знакомы ли вы с правилами здорового сна?
*   **Type:** single
*   **Options:** Да, соблюдаю. Да, но не соблюдаю. Нет

### 13. `q_muscle_symptoms`
*   **Text:** Есть ли судороги, спазмы или онемение?
*   **Type:** multi
*   **Options:** Нет. Судороги ног ночью. Спазмы шеи. Регулярные судороги. Онемение конечностей

### 14. `q_dizziness`
*   **Text:** Испытываете ли вы головокружение?
*   **Type:** single
*   **Options:** Да, часто. Иногда. Нет
*   If answer != "Нет" set flag_anemia
*   If answer != "Нет" set flag_nervous

### 15. `q_pressure`
*   **Text:** Знаете ли вы свое артериальное давление?
*   **Type:** single
*   **Options:** Не знаю. Повышенное. Пониженное. Нестабильное. Есть трекер
*   If answer == "Пониженное" set flag_anemia
*   If answer == "Нестабильное" set flag_anemia

### 16. `q_edema`
*   **Text:** Беспокоят ли вас отеки?
*   **Type:** multi
*   **Options:** Нет. Постоянно. Летом. Ноги. Лицо и руки

### 17. `q_urination`
*   **Text:** Бывают ли стрессовые или ночные позывы к мочеиспусканию?
*   **Type:** single
*   **Options:** Да. Иногда. Нет

### 18. `q_veins`
*   **Text:** Беспокоят ли вас варикоз или тяжесть в ногах?
*   **Type:** single
*   **Options:** Нет. Иногда. Часто

### 19. `q_water`
*   **Text:** Оцените ваш питьевой режим
*   **Type:** multi
*   **Options:** Пью достаточно воды. Пью по приложению. Воду не люблю. Забываю пить. Не чувствую жажды. Пью много

### 20. `q_gut_pain`
*   **Text:** Есть ли боли или дискомфорт в животе?
*   **Type:** multi
*   **Options:** Верх живота. Область пупка. Низ живота. Справа. Слева. Нет

### 21. `q_gut_pain_relation`
*   **Text:** Связаны ли боли с приемом пищи?
*   **Type:** single
*   **Options:** Сразу после еды. Через 1–2 часа. Связаны с голодом. Не связаны. По-разному

### 22. `q_gut_heartburn`
*   **Text:** Беспокоит ли вас изжога?
*   **Type:** single
*   **Options:** Да. Часто. Редко. Нет

### 23. `q_gut_bloating`
*   **Text:** Беспокоит ли вздутие живота?
*   **Type:** single
*   **Options:** Часто. Иногда. Нет

### 24. `q_gut_appetite`
*   **Text:** Как у вас с аппетитом?
*   **Type:** single
*   **Options:** Стабильно хороший. Все время хочется есть. Плохой. Нестабильный

### 25. `q_gut_stool_freq`
*   **Text:** Как часто бывает стул?
*   **Type:** single
*   **Options:** Ежедневный. Несколько раз в день. Не каждый день. Склонность к запорам

### 26. `q_gut_stool_type`
*   **Text:** Характер стула
*   **Type:** single
*   **Options:** Оформленный. Кашицеобразный. Жидкий. Твердый ("овечий"). Чередование

### 27. `q_gut_nausea`
*   **Text:** Бывает ли тошнота?
*   **Type:** single
*   **Options:** Да. Иногда. При укачивании. Нет

### 28. `q_gut_hunger_pain`
*   **Text:** Бывают ли "голодные" боли?
*   **Type:** single
*   **Options:** Да. Нет

### 29. `q_skin_issues`
*   **Text:** Есть ли проблемы с кожей?
*   **Type:** multi
*   **Options:** Сухость. Акне. Высыпания. Жирность. Зуд. Псориаз. Новообразования. Ничего не беспокоит
*   If answer != "Ничего не беспокоит" set flag_skin

### 30. `q_skin_doctor`
*   **Text:** Обращались ли к специалисту?
*   **Type:** single
*   **Options:** Да. Нет. Наблюдаюсь

### 31. `q_dependencies`
*   **Text:** Есть ли зависимости?
*   **Type:** multi
*   **Options:** Нет. Пищевые. Курение. Алкоголь. Игры. Гаджеты. Другое
*   If answer != "Нет" set flag_nervous

### 32. `q_stress_level`
*   **Text:** Оцените уровень стресса от 1 до 10
*   **Type:** single
*   **Options:** 1. 2. 3. 4. 5. 6. 7. 8. 9. 10
*   If answer == "7" set flag_nervous
*   If answer == "8" set flag_nervous
*   If answer == "9" set flag_nervous
*   If answer == "10" set flag_nervous

### 33. `q_memory_problem`
*   **Text:** Есть ли проблемы с памятью?
*   **Type:** single
*   **Options:** Да. Нет
*   If answer == "Да" set flag_nervous

### 34. `q_anemia_weakness`
*   **Text:** Беспокоит ли слабость и быстрая утомляемость?
*   **Type:** single
*   **Options:** Да. Нет

### 35. `q_anemia_skin`
*   **Text:** Есть ли бледность кожи или выпадение волос?
*   **Type:** single
*   **Options:** Да. Нет

### 36. `q_anemia_taste`
*   **Text:** Есть ли тяга к мелу, льду?
*   **Type:** single
*   **Options:** Да. Нет

### 37. `q_anemia_breath`
*   **Text:** Есть ли одышка при легкой нагрузке?
*   **Type:** single
*   **Options:** Да. Нет

### 38. `q_anemia_smell`
*   **Text:** Есть ли тяга к запахам (лак, бензин)?
*   **Type:** single
*   **Options:** Да. Нет

### 39. `q_anemia_cheilitis`
*   **Text:** Есть ли заеды в уголках рта?
*   **Type:** single
*   **Options:** Да. Нет

### 40. `q_anemia_meat`
*   **Text:** Есть ли отвращение к мясу?
*   **Type:** single
*   **Options:** Да. Нет

### 41. `q_anemia_cold`
*   **Text:** Есть ли повышенная зябкость рук и ног?
*   **Type:** single
*   **Options:** Нет. Иногда. Часто

### 42. `q_nervous_memory`
*   **Text:** Как вы оцениваете свою память?
*   **Type:** multi
*   **Options:** Все хорошо. Страдает кратковременная. Плохо удерживаю информацию. Все забываю. Забываю слова

### 43. `q_nervous_tics`
*   **Text:** Есть ли тики или непроизвольные движения?
*   **Type:** single
*   **Options:** Да. Иногда. Нет

### 44. `q_nervous_communication`
*   **Text:** Как вы ощущаете себя в общении?
*   **Type:** single
*   **Options:** Легко общаюсь. Устаю. Предпочитаю одиночество. Не могу без общения

### 45. `q_nervous_emotional`
*   **Text:** Устраивает ли эмоциональное состояние?
*   **Type:** single
*   **Options:** Да. Нет. Наблюдаюсь у специалиста

### 46. `q_nervous_stress_reaction`
*   **Text:** Как реагируете на стресс?
*   **Type:** single
*   **Options:** Адекватно. Остро. С поддержкой препаратов

### 47. `q_nervous_coping`
*   **Text:** Есть ли навыки управления стрессом?
*   **Type:** single
*   **Options:** Да. Нет

### 48. `q_nervous_decisions`
*   **Text:** Легко ли принимаете решения?
*   **Type:** single
*   **Options:** Легко. Сложно. Зависит

### 49. `q_nervous_thinking`
*   **Text:** Устраивает ли умственная работоспособность?
*   **Type:** single
*   **Options:** Устраивает. Не устраивает

### 50. `q_oda_problem`
*   **Text:** Беспокоят ли проблемы опорно-двигательного аппарата?
*   **Type:** single
*   **Options:** Да. Нет. Сейчас нет

### 51. `q_oda_pain`
*   **Text:** Если да, то где локализуется боль?
*   **Type:** multi
*   **Options:** Шея. Спина. Поясница. Суставы. Мышцы

### 52. `q_women_menarche`
*   **Text:** Возраст начала менструации?
*   **Type:** text

### 53. `q_survey_end`
*   **Text:** Спасибо за ответы! Опрос завершен.
*   **Type:** info


## Logic Rules

*   **From `q_gender` (any answer) to `q_occupation`**
*   **From `q_occupation` (any answer) to `q_sport_activity`**
*   **From `q_sport_activity` (any answer) to `q_chronic_diseases`**
*   **From `q_chronic_diseases` (any answer) to `q_family_diseases`**
*   **From `q_family_diseases` (any answer) to `q_surgeries`**
*   **From `q_surgeries` (any answer) to `q_medications`**
*   **From `q_medications` (any answer) to `q_allergy`**
*   **From `q_allergy` (any answer) to `q_orvi`**
*   **From `q_orvi` (any answer) to `q_daily_routine`**
*   **From `q_daily_routine` (any answer) to `q_sleep_quality`**
*   **From `q_sleep_quality` (any answer) to `q_sleep_hygiene`**
*   **From `q_sleep_hygiene` (any answer) to `q_muscle_symptoms`**
*   **From `q_muscle_symptoms` (any answer) to `q_dizziness`**
*   **From `q_dizziness` (any answer) to `q_pressure`**
*   **From `q_pressure` (any answer) to `q_edema`**
*   **From `q_edema` (any answer) to `q_urination`**
*   **From `q_urination` (any answer) to `q_veins`**
*   **From `q_veins` (any answer) to `q_water`**
*   **From `q_water` (any answer) to `q_gut_pain`**

*   **From `q_gut_pain` (answer: Нет) to `q_gut_heartburn`**
*   **From `q_gut_pain` (any answer) to `q_gut_pain_relation`**
*   **From `q_gut_pain_relation` (any answer) to `q_gut_heartburn`**

*   **From `q_gut_heartburn` (any answer) to `q_gut_bloating`**
*   **From `q_gut_bloating` (any answer) to `q_gut_appetite`**
*   **From `q_gut_appetite` (any answer) to `q_gut_stool_freq`**
*   **From `q_gut_stool_freq` (any answer) to `q_gut_stool_type`**
*   **From `q_gut_stool_type` (any answer) to `q_gut_nausea`**
*   **From `q_gut_nausea` (any answer) to `q_gut_hunger_pain`**
*   **From `q_gut_hunger_pain` (any answer) to `q_skin_issues`**

*   **From `q_skin_issues` (flag: flag_skin) to `q_skin_doctor`**
*   **From `q_skin_issues` (any answer) to `q_dependencies`**

*   **From `q_skin_doctor` (any answer) to `q_dependencies`**

*   **From `q_dependencies` (any answer) to `q_stress_level`**
*   **From `q_stress_level` (any answer) to `q_memory_problem`**

*   **From `q_memory_problem` (flag: flag_anemia) to `q_anemia_weakness`**
*   **From `q_memory_problem` (flag: flag_nervous) to `q_nervous_memory`**
*   **From `q_memory_problem` (any answer) to `q_oda_problem`**

*   **From `q_anemia_weakness` (any answer) to `q_anemia_skin`**
*   **From `q_anemia_skin` (any answer) to `q_anemia_taste`**
*   **From `q_anemia_taste` (any answer) to `q_anemia_breath`**
*   **From `q_anemia_breath` (any answer) to `q_anemia_smell`**
*   **From `q_anemia_smell` (any answer) to `q_anemia_cheilitis`**
*   **From `q_anemia_cheilitis` (any answer) to `q_anemia_meat`**
*   **From `q_anemia_meat` (any answer) to `q_anemia_cold`**

*   **From `q_anemia_cold` (flag: flag_nervous) to `q_nervous_memory`**
*   **From `q_anemia_cold` (any answer) to `q_oda_problem`**

*   **From `q_nervous_memory` (any answer) to `q_nervous_tics`**
*   **From `q_nervous_tics` (any answer) to `q_nervous_communication`**
*   **From `q_nervous_communication` (any answer) to `q_nervous_emotional`**
*   **From `q_nervous_emotional` (any answer) to `q_nervous_stress_reaction`**
*   **From `q_nervous_stress_reaction` (any answer) to `q_nervous_coping`**
*   **From `q_nervous_coping` (any answer) to `q_nervous_decisions`**
*   **From `q_nervous_decisions` (any answer) to `q_nervous_thinking`**
*   **From `q_nervous_thinking` (any answer) to `q_oda_problem`**

*   **From `q_oda_problem` (answer: Да) to `q_oda_pain`**
*   **From `q_oda_problem` (answer: Женщина) to `q_women_menarche`**
*   **From `q_oda_problem` (any answer) to `q_survey_end`**

*   **From `q_oda_pain` (answer: Женщина) to `q_women_menarche`**
*   **From `q_oda_pain` (any answer) to `q_survey_end`**

*   **From `q_women_menarche` (any answer) to `q_survey_end`**
