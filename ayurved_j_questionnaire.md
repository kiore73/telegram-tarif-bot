# Ayurved Female Questionnaire Specification

## Overview
This document specifies the "ayurved_j" questionnaire, which is a gender-specific questionnaire for females, designed to gather information relevant to Ayurvedic constitution analysis.

## Questions

### 1. `constitution_body_type`
*   **Text:** Какое описание телосложения вам подходит больше всего?
*   **Type:** single
*   **Options:** Высокий или низкий рост. худоба. плохо развитое тело. Средний рост или выше среднего. Низкий рост. крепкое. хорошо развитое тело

### 2. `constitution_weight`
*   **Text:** Как вы бы описали свой вес?
*   **Type:** single
*   **Options:** Небольшой. дефицит жировой и мышечной массы. Умеренный. легко набираю и сбрасываю вес. Склонность к набору жировой массы

### 3. `constitution_bones`
*   **Text:** Какие у вас кости?
*   **Type:** single
*   **Options:** Лёгкие. тонкие. выступающие суставы. Нормальная костная система. Массивная костная система

### 4. `constitution_skin_color`
*   **Text:** Какой у вас цвет кожи?
*   **Type:** single
*   **Options:** Темная. пигментные или родимые пятна. Светлая. легко краснеет. веснушки. Белая. молочная. ровная

### 5. `constitution_skin_type`
*   **Text:** Какая у вас кожа?
*   **Type:** single
*   **Options:** Тонкая. сухая. шершавая. Влажная. легко потеет. склонна к воспалениям. Толстая. жирная. мягкая

### 6. `constitution_thermoregulation`
*   **Text:** Как вы переносите температуру?
*   **Type:** single
*   **Options:** Часто мерзну. холодные руки и ноги. Часто жарко. бросает в тепло. Прохладное тело. стабильная температура

### 7. `constitution_hair`
*   **Text:** Какие у вас волосы?
*   **Type:** single
*   **Options:** Сухие. ломкие. тонкие. редкие. Прямые. жирные. мягкие. склонны к ранней седине. Густые. пышные. маслянистые. блестящие

### 8. `constitution_head`
*   **Text:** Размер головы
*   **Type:** single
*   **Options:** Небольшая. Средняя. Большая. крепко посаженная

### 9. `constitution_face`
*   **Text:** Форма лица
*   **Type:** single
*   **Options:** Удлиненное. угловатое. Сердцевидное. Круглое или квадратное

### 10. `constitution_forehead`
*   **Text:** Лоб
*   **Type:** single
*   **Options:** Узкий. маленький. Средний. Широкий. большой

### 11. `constitution_eyebrows`
*   **Text:** Брови
*   **Type:** single
*   **Options:** Редкие, неровные. Умеренно густые. Густые, плотные

### 12. `constitution_eyelashes`
*   **Text:** Ресницы
*   **Type:** single
*   **Options:** Маленькие, сухие. Средние, мягкие. Большие, густые

### 13. `constitution_eyes`
*   **Text:** Глаза
*   **Type:** single
*   **Options:** Подвижный, бегающий взгляд. Острый, пронизывающий взгляд. Спокойный, мягкий взгляд

### 14. `constitution_nose`
*   **Text:** Нос
*   **Type:** single
*   **Options:** Тонкий, изогнутый. Средний, острый. Короткий, округлый

### 15. `constitution_cheeks`
*   **Text:** Щёки
*   **Type:** single
*   **Options:** Впалые. Средние. Округлые, полные

### 16. `constitution_lips`
*   **Text:** Губы
*   **Type:** single
*   **Options:** Тонкие, сухие. Средние, мягкие. Пухлые, объемные

### 17. `constitution_teeth`
*   **Text:** Зубы
*   **Type:** single
*   **Options:** Неровные, чувствительные. Средние, чувствительны к кислому. Крупные, плотные, белые

### 18. `constitution_chin`
*   **Text:** Подбородок
*   **Type:** single
*   **Options:** Тонкий, угловатый. Заостренный. Округлый, массивный

### 19. `constitution_neck`
*   **Text:** Шея
*   **Type:** single
*   **Options:** Тонкая, длинная. Средняя. Короткая, объемная

### 20. `constitution_shoulders`
*   **Text:** Плечи
*   **Type:** single
*   **Options:** Узкие. Средние. Широкие

### 21. `constitution_chest`
*   **Text:** Грудная клетка
*   **Type:** single
*   **Options:** Узкая, плоская. Средняя. Широкая, округлая

### 22. `constitution_voice`
*   **Text:** Голос
*   **Type:** single
*   **Options:** Низкий, слабый. Резкий, высокий. Глубокий, мелодичный

### 23. `constitution_speech`
*   **Text:** Речь
*   **Type:** single
*   **Options:** Быстрая, сбивчивая. Четкая, аргументированная. Медленная, спокойная

### 24. `constitution_stress`
*   **Text:** Реакция на стресс
*   **Type:** single
*   **Options:** Страх, тревожность. Гнев, раздражение. Апатия, подавленность

### 25. `constitution_forgiveness`
*   **Text:** Прощение
*   **Type:** single
*   **Options:** Легко прощаю. Прощаю после извинений. Прощаю с трудом

## Logic Rules
The questions in this questionnaire are presented sequentially, without complex branching logic based on specific answers. Each question directly follows the previous one.
