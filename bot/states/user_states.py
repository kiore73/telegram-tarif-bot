from aiogram.fsm.state import State, StatesGroup


class BookingFSM(StatesGroup):
    choosing_tariff = State()
    awaiting_payment = State()
    entering_first_name = State()
    entering_last_name = State()
    entering_age = State()
    entering_weight = State()
    choosing_gender = State()        # only lite tariff
    answering_questionnaire = State()
    uploading_photos = State()
    choosing_slot = State()
    confirming_booking = State()


class AdminFSM(StatesGroup):
    main_menu = State()
    entering_slot_date = State()
    entering_slot_time = State()
    entering_slot_duration = State()
    confirming_slot = State()
    deleting_slot = State()
