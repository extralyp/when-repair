import pandas as pd

def find_nearest_value(user_input, key_value_dict):
    closest_key = None
    closest_value = None

    for key, value in key_value_dict.items():
        if closest_key is None or abs(user_input - key) < abs(user_input - closest_key):
            closest_key = key
            closest_value = value

    return closest_key, closest_value

def calculate_V_cor(Cl, HCO3, CA, pH, vl, v_cr, p,d):
    # Определение словарей с коэффициентами (оставлены те же самые)
    # Задаем словарь с коэффициентами Kv_ot
    def get_Kv_ot(d):
        if d <= 377:
            return {
                0.1: 0.8,
                0.2: 0.4,
                0.3: 0.5,
                1.4: 1.2,
                0.5: 0.6,
                0.6: 0.7,
                0.7: 0.5,
                0.8: 0.9,
                0.9: 0.4,
                1.0: 0.4,
                1.2: 0.08,
                2.0: 0.04,
                2.2: 0.06
            }
        elif d <= 530:
            return {
                0.1: 0.8,
                0.2: 0.5,
                0.3: 0.7,
                1.4: 0.6,
                0.5: 0.8,
                0.6: 1.5,
                0.7: 0.7,
                0.8: 0.6,
                0.9: 0.6,
                1.0: 0.3,
                1.2: 0.08,
                2.0: 0.07,
                2.2: 0.06
            }
        else:
            return {
                0.1: 1.0,
                0.2: 0.6,
                0.3: 0.7,
                1.4: 1.0,
                0.5: 1.4,
                0.6: 1.0,
                0.7: 0.6,
                0.8: 0.3,
                0.9: 0.3,
                1.0: 0.3,
                1.2: 0.06,
                2.0: 0.06,
                2.2: 0.06
            }

    # Остальные словари с коэффициентами
    Kcl = {
        6: 0.9,
        8: 1.0,
        10: 1.1,
        12: 1.15,
        14: 1.2,
        16: 1.25,
        18: 1.3,
        20: 1.3,
        22: 1.3
    }
    Khco3 = {
        100: 0.6,
        200: 0.8,
        400: 1.0,
        600: 1.15,
        800: 1.3,
        1000: 1.4,
        1200: 1.5,
        1400: 1.6,
        1600: 1.7,
        2000: 1.75
    }
    Kca = {
        100: 0.85,
        200: 0.9,
        300: 0.95,
        400: 1.0,
        500: 1.05,
        600: 1.1,
        700: 1.15,
        800: 1.2,
        900: 1.2,
        1000: 1.2
    }
    KpH = {
        6.0: 0.85,
        6.5: 0.9,
        7.0: 0.95,
        7.5: 1.0,
        8.0: 1.05,
        8.5: 1.1
    }
    Kv = {
        1: 0.6,
        1.1: 0.8,
        1.3: 0.9,
        1.6: 1.0,
        2.0: 1.1,
        2.2: 1.15,
        2.5: 1.2,
        3: 1.25,
        3.3: 1.3
    }
    Kp = {
        0.2: 0.6,
        0.4: 0.8,
        0.6: 0.9,
        0.8: 1.0,
        1.0: 1.1,
        1.2: 1.15,
        1.4: 1.2,
        1.6: 1.25,
        1.8: 1.3,
        2.0: 1.3
    }

    # Вычисление отношения ot
    ot = vl / v_cr

    # Вызов функции find_nearest_value для каждого словаря
    Kv_ot = get_Kv_ot(d)
    closest_key_Kv_ot, closest_value_Kv_ot = find_nearest_value(ot, Kv_ot)

    closest_key_Kcl, closest_value_Kcl = find_nearest_value(Cl, Kcl)
    closest_key_Khco3, closest_value_Khco3 = find_nearest_value(HCO3, Khco3)
    closest_key_Kca, closest_value_Kca = find_nearest_value(CA, Kca)
    closest_key_KpH, closest_value_KpH = find_nearest_value(pH, KpH)
    closest_key_Kv, closest_value_Kv = find_nearest_value(vl, Kv)
    closest_key_Kp, closest_value_Kp = find_nearest_value(p, Kp)

    # Вычисление V_cor
    Kchem = closest_value_Kca * closest_value_Khco3 * closest_value_Kcl * closest_value_KpH
    K2 = closest_value_Kp * closest_value_Kv * closest_value_Kv_ot
    V_cor = Kchem * K2

    return V_cor + 0.065

