import random
from aiogram import Router, F
from aiogram.types import Message
from keyboards import reply, fabrics
from data.subloader import get_json

router = Router()


@router.message()
async def msg(message: Message):
    msg = message.text.lower()
    bags = await get_json('bags.json')
    cloth = await get_json('cloth.json')
    cosmetics = await get_json('cosmetics.json')
    electronic_equipment = await get_json('electronic_equipment.json')
    medicines = await get_json('medicines.json')
    random_fact = await get_json('random.json')

    if msg == 'отпуск':
        await message.answer('Отлично! Давайте скорее соберем вещи!', reply_markup=reply.vacation_kb)
    elif msg == 'ежедневник':
        await message.answer('Ничего не забудьте!', reply_markup=reply.dairy_kb)
    elif msg == 'список заметок':
        await message.answer('Список ваших заметок: ', reply_markup=reply.list_dairy_kb)
    elif msg == 'новая заметка':
        await message.answer('Создадим новую заметку!', reply_markup=reply.call_dairy_kb)
    elif msg == 'назад':
        await message.answer('Главное меню', reply_markup=reply.main_kb)
    elif msg == 'предупредить начальство':
        await message.answer('Давай создадим задачу и я о ней напомню!\n'
                             'Введите дату и время события в формате YYYY-MM-DD HH:MM:SS.', reply_markup=reply.call_kb)
    elif msg == 'начать отсчет':
        await message.answer(f'Как здорово, {message.from_user.username}! '
                             f'Когда планируем отдыхать?\n'
                             f'Введите дату и время события в формате YYYY-MM-DD HH:MM:SS.', reply_markup=reply.call_kb)
    elif msg == 'собрать вещи':
        await message.answer('Отлично! Давай приступим!', reply_markup=reply.bags_kb)
    elif msg == 'документы':
        await message.answer(f'{bags[0][0]} {bags[0][1]}', reply_markup=fabrics.pag())
        if bags:
            await message.answer('Подсказка: '
                                 'Некоторые документы можно отсканировать!', reply_markup=reply.bags_kb)
    elif msg == 'одежда':
        await message.answer(f'{cloth[0][0]} {cloth[0][1]}', reply_markup=fabrics.pag())
        if cloth:
            await message.answer('Подсказка: '
                                 'Головной убор очень важен!\n'
                                 'Для холодных стиран не забудьте термобелье!', reply_markup=reply.bags_kb)
    elif msg == 'косметика':
        await message.answer(f'{cosmetics[0][0]} {cosmetics[0][1]}', reply_markup=fabrics.pag())
        if cosmetics:
            await message.answer('Подсказка: '
                                 'Убедитесь, что такие объемы жидкости можно провозить!', reply_markup=reply.bags_kb)
    elif msg == 'лекарства':
        await message.answer(f'{medicines[0][0]} {medicines[0][1]}', reply_markup=fabrics.pag())
        if medicines:
            await message.answer('Подсказка: '
                                 'Не забывайте заботиться о своем пищеварении!', reply_markup=reply.bags_kb)
    elif msg == 'техника':
        await message.answer(f'{electronic_equipment[0][0]} {electronic_equipment[0][1]}', reply_markup=fabrics.pag())
        if electronic_equipment:
            await message.answer('Подсказка: '
                                 'Проверь наличие всех проводов для зарядки своих устройств. '
                                 'Их может не хватить!', reply_markup=reply.bags_kb)
    elif msg == 'интересный факт':
        await message.answer(f'{random_fact[0][0]} {random_fact[0][1]}', reply_markup=fabrics.pag())
