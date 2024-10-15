from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards import fabrics
from data.subloader import get_json


router = Router()


@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev', 'next'])))
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    bags = await get_json('bags.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(bags) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{bags[page][0]} {bags[page][1]}',
            reply_markup=fabrics.pag(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev', 'next'])))
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    cloth = await get_json('cloth.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(cloth) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{cloth[page][0]} {cloth[page][1]}',
            reply_markup=fabrics.pag(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev', 'next'])))
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    cosmetics = await get_json('cosmetics.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(cosmetics) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{cosmetics[page][0]} {cosmetics[page][1]}',
            reply_markup=fabrics.pag(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev', 'next'])))
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    electronic_equipment = await get_json('electronic_equipment.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(electronic_equipment) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{electronic_equipment[page][0]} {electronic_equipment[page][1]}',
            reply_markup=fabrics.pag(page)
        )
    await call.answer()

@router.callback_query(fabrics.Pag.filter(F.action.in_(['prev', 'next'])))
async def pagination(call: CallbackQuery, callback_data: fabrics.Pag):
    medicines = await get_json('medicines.json')

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(medicines) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f'{medicines[page][0]} {medicines[page][1]}',
            reply_markup=fabrics.pag(page)
        )
    await call.answer()
