# Basic Questionnaire Specification

## Overview
This document specifies the "basic" questionnaire, including its questions, options, and branching logic. This questionnaire is designed to gather general health and lifestyle information from the user.

## Questions

### 1. `q_gender`
*   **Text:** Укажите ваш пол
*   **Type:** single
*   **Options:** Мужчина. Женщина

### 2. `q_occupation`
*   **Text:** Ваш род занятий, работа (можно выбрать несколько вариантов)
*   **Type:** multi
*   **Options:** Сидячая. Присутствует физическая нагрузка. Высокая умственная нагрузка / высокий уровень ответственности. Приходится долго стоять. Много разъездов, поездок, перелетов

### 3. `q_sport_activity`
*   **Text:** Присутствуют ли в вашей жизни спорт или физическая активность?
*   **Type:** single
*   **Options:** Да, регулярно. Нерегулярно, время от времени. Нет и не было. Я профессиональный спортсмен

### 4. `q_chronic_diseases`
*   **Text:** Если у вас есть или были хронические или наследственные заболевания, укажите диагнозы
*   **Type:** text

### 5. `q_family_diseases`
*   **Text:** Есть ли хронические или генетические заболевания у ваших ближайших биологических родственников?
*   **Type:** text

### 6. `q_surgeries`
*   **Text:** Были ли у вас операции? Если да, какие и как давно?
*   **Type:** text

### 7. `q_medications`
*   **Text:** Принимаете ли вы на постоянной основе фармацевтические препараты или БАДы? Если да, укажите какие
*   **Type:** text

### 8. `q_allergy`
*   **Text:** Испытываете ли вы симптомы аллергии?
*   **Type:** single
*   **Options:** Очень часто. Иногда. Сезонно. Нет

### 9. `q_orvi`
*   **Text:** Как часто вы переносите сезонные ОРВИ?
*   **Type:** single
*   **Options:** Очень редко. 1–2 раза в год. 3–4 раза в год. Постоянно, даже летом

### 10. `q_daily_routine`
*   **Text:** Опишите кратко ваш режим дня (сон, питание, работа, транспорт, хобби, прогулки)
*   **Type:** text

### 11. `q_sleep_quality`
*   **Text:** Оцените качество вашего сна (можно выбрать несколько вариантов)
*   **Type:** multi
*   **Options:** Быстро засыпаю. Требуется более 40 минут для засыпания. Сон без пробуждений. Сон чуткий, есть пробуждения. Есть трекер сна. Просыпаюсь легко и чувствую восстановление. Просыпаюсь тяжело, но потом бодр. Тяжело проснуться, нет сил до обеда

### 12. `q_sleep_hygiene`
*   **Text:** Знакомы ли вы с правилами и гигиеной здорового сна?
*   **Type:** single
*   **Options:** Да, стараюсь придерживаться. Да, но не получается соблюдать. Нет, не знаком

### 13. `q_muscle_symptoms`
*   **Text:** Наблюдали ли вы у себя мышечные судороги, слабость или онемение?
*   **Type:** multi
*   **Options:** Нет. Судороги ног ночью. Спазмы мышц шеи. Судороги или спазмы регулярно. Онемение конечностей

### 14. `q_dizziness`
*   **Text:** Испытываете ли вы головокружение?
*   **Type:** single
*   **Options:** Да, часто. Иногда. Нет

### 15. `q_pressure`
*   **Text:** Знаете ли вы свое артериальное давление и пульс?
*   **Type:** single
*   **Options:** Не знаю. Повышенное / гипертония. Пониженное. Нестабильное. Есть трекер

### 16. `q_edema`
*   **Text:** Беспокоят ли вас отеки?
*   **Type:** multi
*   **Options:** Нет. Постоянно. Летом, отекают ноги/лодыжки. Лицо и руки

### 17. `q_urination`
*   **Text:** Бывают ли стрессовые или ночные позывы к мочеиспусканию?
*   **Type:** single
*   **Options:** Да. Иногда. Нет

### 18. `q_veins`
*   **Text:** Беспокоят ли вас вены, сосудистые звездочки, варикоз, тяжесть в ногах?
*   **Type:** single
*   **Options:** Нет, беспокоит тяжесть. Часто

### 19. `q_water`
*   **Text:** Оцените ваш питьевой режим
*   **Type:** multi
*   **Options:** Пью достаточно воды. Воду не люблю, пью другие напитки. Забываю пить, часто жажда. Не чувствую жажды. Пью много, жажда не утоляется

### 20. `q_gut_pain`
*   **Text:** Испытываете ли вы болевые ощущения или дискомфорт в животе?
*   **Type:** multi
*   **Options:** В верхней части живота (эпигастрий). В области пупка. Внизу живота. Больше справа. Больше слева или в области спины. Нет

### 21. `q_gut_pain_relation`
*   **Text:** Если есть боли, связаны ли они с приемом пищи?
*   **Type:** single
*   **Options:** Сразу после еды. В течение 1–2 часов. Связаны с голодом. Не связаны. Бывает по-разному

### 22. `q_gut_heartburn`
*   **Text:** Беспокоят ли вас изжога, жжение за грудиной, отрыжка, нарушение глотания?
*   **Type:** single
*   **Options:** Часто. Иногда. Нет

### 23. `q_gut_bloating`
*   **Text:** Беспокоят ли вас вздутие живота или метеоризм?
*   **Type:** single
*   **Options:** Нет. Иногда. Постоянно

### 24. `q_gut_appetite`
*   **Text:** Оцените ваш аппетит
*   **Type:** single
*   **Options:** Стабильно хороший. Все время хочется есть. Плохой. Нестабильный

### 25. `q_gut_stool_regular`
*   **Text:** Какая регулярность стула?
*   **Type:** single
*   **Options:** Ежедневный по утрам. Ежедневный в разное время. Несколько раз в сутки. Непредсказуемый. Не каждый день

### 26. `q_gut_stool_type`
*   **Text:** Оцените характер стула
*   **Type:** single
*   **Options:** Нормальный, оформленный. Склонность к диарее. Очень плотный. Нестабильный. Есть примеси

### 27. `q_gut_nausea`
*   **Text:** Испытываете ли вы тошноту?
*   **Type:** multi
*   **Options:** Бывает иногда. На определенные продукты. Очень редко. При укачивании

### 28. `q_gut_hunger_break`
*   **Text:** Как вы переносите длительные перерывы между приемами пищи?
*   **Type:** single
*   **Options:** Нормально. Появляется слабость, головокружение. Очень плохо

### 29. `q_gut_sleep_after_food`
*   **Text:** Испытываете ли вы сонливость после еды?
*   **Type:** single
*   **Options:** Да. Нет. Бывает редко

### 30. `q_gut_food_intolerance`
*   **Text:** Есть ли продукты, после которых вы замечаете ухудшение самочувствия?
*   **Type:** single
*   **Options:** Да. Нет

### 31. `q_skin_issues`
*   **Text:** Что вас не устраивает в состоянии кожи? (можно выбрать несколько вариантов)
*   **Type:** multi
*   **Options:** Сухость, раздражение. Изменение цвета. Высыпания, дерматиты. Акне. Повышенная жирность. Папилломы, родинки. Бородавки. Потеря упругости. Стрии. Зуд. Возрастные изменения. Отечность. Витилиго. Псориаз. Новообразования. Грибок

### 32. `q_skin_doctor`
*   **Text:** Обращались ли вы к специалисту по поводу кожи?
*   **Type:** single
*   **Options:** Да. Нет. Постоянно наблюдаюсь

### 33. `q_nervous_problem_question`
*   **Text:** Есть ли у вас проблемы с нервной системой или повышенный уровень стресса?
*   **Type:** single
*   **Options:** Да. Нет

### 34. `q_nervous_memory`
*   **Text:** Как вы оцениваете свою память?
*   **Type:** multi
*   **Options:** Все хорошо. Страдает кратковременная память. Плохо удерживаю информацию. Все забываю. Забываю слова и имена

### 35. `q_nervous_tics`
*   **Text:** Наблюдаете ли вы тики или непроизвольные движения?
*   **Type:** single
*   **Options:** Да. Иногда. Нет

### 36. `q_nervous_communication`
*   **Text:** Как вы ощущаете себя в общении с людьми?
*   **Type:** single
*   **Options:** Легко общаюсь. Устаю от общения. Предпочитаю одиночество. Не могу без общения

### 37. `q_nervous_emotional`
*   **Text:** Устраивает ли вас ваше эмоциональное состояние?
*   **Type:** single
*   **Options:** Да. Нет. Наблюдаюсь у специалиста

### 38. `q_nervous_stress_reaction`
*   **Text:** Как вы реагируете на стресс?
*   **Type:** single
*   **Options:** Адекватно. Остро. С поддержкой препаратов

### 39. `q_nervous_coping`
*   **Text:** Есть ли у вас навыки управления стрессом?
*   **Type:** single
*   **Options:** Да. Нет

### 40. `q_nervous_decisions`
*   **Text:** Насколько легко вам принимать решения?
*   **Type:** single
*   **Options:** Легко. Сложно. Зависит от ситуации

### 41. `q_nervous_thinking`
*   **Text:** Устраивает ли вас уровень мышления и умственной работоспособности?
*   **Type:** single
*   **Options:** Устраивает. Не устраивает

### 42. `q_anemia_weakness`
*   **Text:** Беспокоит ли вас слабость или быстрая утомляемость?
*   **Type:** single
*   **Options:** Да. Нет

### 43. `q_anemia_skin`
*   **Text:** Замечаете ли вы бледность кожи или выпадение волос?
*   **Type:** single
*   **Options:** Да. Нет

### 44. `q_anemia_taste`
*   **Text:** Бывают ли необычные вкусовые желания (мел, лед и т.п.)?
*   **Type:** single
*   **Options:** Да. Нет

### 45. `q_anemia_breath`
*   **Text:** Бывает ли одышка или учащенное сердцебиение при легкой нагрузке?
*   **Type:** single
*   **Options:** Да. Нет

### 46. `q_anemia_smell`
*   **Text:** Есть ли тяга к необычным запахам (лак, бензин и т.п.)?
*   **Type:** single
*   **Options:** Да. Нет

### 47. `q_anemia_cheilitis`
*   **Text:** Беспокоят ли заеды в углах рта?
*   **Type:** single
*   **Options:** Да. Нет

### 48. `q_anemia_meat`
*   **Text:** Есть ли отвращение к мясу или продуктам?
*   **Type:** single
*   **Options:** Да. Нет

### 49. `q_anemia_cold`
*   **Text:** Отмечаете ли повышенную зябкость рук и ног?
*   **Type:** single
*   **Options:** Да. Нет

### 50. `q_oda_pain`
*   **Text:** Беспокоят ли вас болевые ощущения?
*   **Type:** multi
*   **Options:** Голова. Шея. Спина. Поясница. Суставы

### 51. `q_oda_pain_level`
*   **Text:** Оцените интенсивность боли по шкале от 1 до 10
*   **Type:** text

### 52. `q_oda_stiffness`
*   **Text:** Есть ли скованность или тугоподвижность суставов?
*   **Type:** single
*   **Options:** Да. Нет

### 53. `q_oda_diagnosis`
*   **Text:** Есть ли диагностированные заболевания ОДА (грыжи, артрит и т.п.)?
*   **Type:** single
*   **Options:** Да. Нет

### 54. `q_oda_feet`
*   **Text:** Есть ли патологии стопы?
*   **Type:** single
*   **Options:** Да. Нет

### 55. `q_oda_shoes`
*   **Text:** Изменился ли размер обуви?
*   **Type:** single
*   **Options:** Да. Нет

### 56. `q_oda_doctor`
*   **Text:** Обращались ли вы к специалисту?
*   **Type:** multi
*   **Options:** Да. Нет

### 57. `q_women_menarche`
*   **Text:** Укажите, по возможности, возраст начала первой менструации (менархе)
*   **Type:** text

### 58. `q_women_cycle_status`
*   **Text:** Какое у вас текущее состояние менструального цикла?
*   **Type:** single
*   **Options:** Регулярный. Нерегулярный. Отсутствует. Менопауза. Беременность. Лактация

### 59. `q_women_pregnancy`
*   **Text:** Были ли у вас беременности или роды?
*   **Type:** single
*   **Options:** Да. Нет

### 60. `q_women_cycle_length`
*   **Text:** Укажите продолжительность цикла от первого дня менструации до последнего дня цикла (в днях)
*   **Type:** text

### 61. `q_women_menses_length`
*   **Text:** Укажите среднюю продолжительность менструации
*   **Type:** single
*   **Options:** 1-2 дня. 3-5 дней, более 5 дней

### 62. `q_women_pms`
*   **Text:** Беспокоят ли вас симптомы ПМС? (можно выбрать несколько вариантов)
*   **Type:** multi
*   **Options:** Раздражительность. Плаксивость. Боль внизу живота. Набухание молочных желез. Головная боль. Слабость. Отсутствует

### 63. `q_women_sleep_menses`
*   **Text:** Замечаете ли вы проблемы со сном накануне или во время менструации?
*   **Type:** single
*   **Options:** Да. Нет

### 64. `q_women_flow_amount`
*   **Text:** Оцените обильность менструальных выделений по шкале от 1 до 10
*   **Type:** text

### 65. `q_women_pain_level`
*   **Text:** Оцените болезненность во время менструации по шкале от 1 до 10
*   **Type:** text

### 66. `q_women_flow_type`
*   **Text:** Как вы можете описать менструальные выделения?
*   **Type:** single
*   **Options:** Обильные. Умеренные. Скудные

### 67. `q_women_gut_menses`
*   **Text:** Бывает ли дискомфорт со стороны ЖКТ во время или накануне менструации?
*   **Type:** single
*   **Options:** Да. Нет

### 68. `q_women_bleeding_other_days`
*   **Text:** Бывают ли кровянистые выделения в другие дни цикла?
*   **Type:** single
*   **Options:** Да. Нет

### 69. `q_women_cystitis`
*   **Text:** Бывают ли у вас проявления цистита?
*   **Type:** single
*   **Options:** Да. Нет

### 70. `q_women_candidiasis`
*   **Text:** Беспокоят ли проявления молочницы (кандидоза)?
*   **Type:** single
*   **Options:** Да. Нет

### 71. `q_women_cosmetics_amount`
*   **Text:** Сколько уходовых средств вы используете ежедневно? (для лица, тела, волос)
*   **Type:** single
*   **Options:** 3–4 и менее. 5–8. Около 10. Более 10

### 72. `q_women_ecology`
*   **Text:** Ваш запрос связан с экологией?
*   **Type:** single
*   **Options:** Да. Нет. Не в первую очередь

### 73. `q_survey_end`
*   **Text:** Спасибо за ответы! На этом базовый опросник завершен.
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
*   **From `q_gut_pain` (any answer) to `q_gut_pain_relation`**
*   **From `q_gut_pain_relation` (any answer) to `q_gut_heartburn`**
*   **From `q_gut_heartburn` (any answer) to `q_gut_bloating`**
*   **From `q_gut_bloating` (any answer) to `q_gut_appetite`**
*   **From `q_gut_appetite` (any answer) to `q_gut_stool_regular`**
*   **From `q_gut_stool_regular` (any answer) to `q_gut_stool_type`**
*   **From `q_gut_stool_type` (any answer) to `q_gut_nausea`**
*   **From `q_gut_nausea` (any answer) to `q_gut_hunger_break`**
*   **From `q_gut_hunger_break` (any answer) to `q_gut_sleep_after_food`**
*   **From `q_gut_sleep_after_food` (any answer) to `q_gut_food_intolerance`**
*   **From `q_gut_food_intolerance` (any answer) to `q_skin_issues`**
*   **From `q_skin_issues` (any answer) to `q_skin_doctor`**
*   **From `q_skin_doctor` (any answer) to `q_nervous_problem_question`**
*   **From `q_nervous_problem_question` (any answer) to `q_nervous_memory`**
*   **From `q_nervous_memory` (any answer) to `q_nervous_tics`**
*   **From `q_nervous_tics` (any answer) to `q_nervous_communication`**
*   **From `q_nervous_communication` (any answer) to `q_nervous_emotional`**
*   **From `q_nervous_emotional` (any answer) to `q_nervous_stress_reaction`**
*   **From `q_nervous_stress_reaction` (any answer) to `q_nervous_coping`**
*   **From `q_nervous_coping` (any answer) to `q_nervous_decisions`**
*   **From `q_nervous_decisions` (any answer) to `q_nervous_thinking`**
*   **From `q_nervous_thinking` (any answer) to `q_anemia_weakness`**
*   **From `q_anemia_weakness` (any answer) to `q_anemia_skin`**
*   **From `q_anemia_skin` (any answer) to `q_anemia_taste`**
*   **From `q_anemia_taste` (any answer) to `q_anemia_breath`**
*   **From `q_anemia_breath` (any answer) to `q_anemia_smell`**
*   **From `q_anemia_smell` (any answer) to `q_anemia_cheilitis`**
*   **From `q_anemia_cheilitis` (any answer) to `q_anemia_meat`**
*   **From `q_anemia_meat` (any answer) to `q_anemia_cold`**
*   **From `q_anemia_cold` (any answer) to `q_oda_pain`**
*   **From `q_oda_pain` (any answer) to `q_oda_pain_level`**
*   **From `q_oda_pain_level` (any answer) to `q_oda_stiffness`**
*   **From `q_oda_stiffness` (any answer) to `q_oda_diagnosis`**
*   **From `q_oda_diagnosis` (any answer) to `q_oda_feet`**
*   **From `q_oda_feet` (any answer) to `q_oda_shoes`**
*   **From `q_oda_shoes` (any answer) to `q_oda_doctor`**
*   **From `q_oda_doctor` (answer: Мужчина) to `q_survey_end`**
*   **From `q_oda_doctor` (answer: Женщина) to `q_women_menarche`**
*   **From `q_women_menarche` (any answer) to `q_women_cycle_status`**
*   **From `q_women_cycle_status` (any answer) to `q_women_pregnancy`**
*   **From `q_women_pregnancy` (any answer) to `q_women_cycle_length`**
*   **From `q_women_cycle_length` (any answer) to `q_women_menses_length`**
*   **From `q_women_menses_length` (any answer) to `q_women_pms`**
*   **From `q_women_pms` (any answer) to `q_women_sleep_menses`**
*   **From `q_women_sleep_menses` (any answer) to `q_women_flow_amount`**
*   **From `q_women_flow_amount` (any answer) to `q_women_pain_level`**
*   **From `q_women_pain_level` (any answer) to `q_women_flow_type`**
*   **From `q_women_flow_type` (any answer) to `q_women_gut_menses`**
*   **From `q_women_gut_menses` (any answer) to `q_women_bleeding_other_days`**
*   **From `q_women_bleeding_other_days` (any answer) to `q_women_cystitis`**
*   **From `q_women_cystitis` (any answer) to `q_women_candidiasis`**
*   **From `q_women_candidiasis` (any answer) to `q_women_cosmetics_amount`**
*   **From `q_women_cosmetics_amount` (any answer) to `q_women_ecology`**
*   **From `q_women_ecology` (any answer) to `q_survey_end`**