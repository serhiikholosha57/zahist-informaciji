import re
from datetime import datetime

def get_personal_data():
    name = input("Введіть ім'я: ").strip()
    surname = input("Введіть прізвище: ").strip()
    birth_date = input("Введіть дату народження (ДД.ММ.РРРР): ").strip()
    password = input("Введіть пароль: ").strip()
    return name, surname, birth_date, password

def extract_date_components(birth_date):
    try:
        date_obj = datetime.strptime(birth_date, "%d.%m.%Y")
        return {
            'day': str(date_obj.day).zfill(2),
            'month': str(date_obj.month).zfill(2),
            'year': str(date_obj.year),
            'year_short': str(date_obj.year)[2:]
        }
    except:
        return None

def check_personal_data_in_password(password, name, surname, date_parts):
    issues = []
    password_lower = password.lower()
    
    if name.lower() in password_lower:
        issues.append(f"містить ім'я '{name}'")
    
    if surname.lower() in password_lower:
        issues.append(f"містить прізвище '{surname}'")
    
    if date_parts:
        if date_parts['year'] in password:
            issues.append(f"містить рік народження '{date_parts['year']}'")
        if date_parts['year_short'] in password:
            issues.append(f"містить рік '{date_parts['year_short']}'")
        if date_parts['day'] in password:
            issues.append(f"містить день '{date_parts['day']}'")
        if date_parts['month'] in password:
            issues.append(f"містить місяць '{date_parts['month']}'")
    
    return issues

def evaluate_password_strength(password):
    score = 0
    criteria = []
    
    length = len(password)
    if length >= 12:
        score += 3
        criteria.append("достатня довжина")
    elif length >= 8:
        score += 2
        criteria.append("прийнятна довжина")
    else:
        score += 1
        criteria.append("недостатня довжина")
    
    if re.search(r'[a-z]', password):
        score += 1
        criteria.append("є малі літери")
    
    if re.search(r'[A-Z]', password):
        score += 1
        criteria.append("є великі літери")
    
    if re.search(r'\d', password):
        score += 1
        criteria.append("є цифри")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 2
        criteria.append("є спеціальні символи")
    
    common_patterns = ['123', 'qwerty', 'password', 'admin', 'user', 'pass']
    has_common = any(pattern in password.lower() for pattern in common_patterns)
    if has_common:
        score -= 2
        criteria.append("містить поширені комбінації")
    
    return max(1, min(10, score)), criteria

def generate_recommendations(password, personal_issues, strength_score):
    recommendations = []
    
    if personal_issues:
        recommendations.append("Уникайте використання особистих даних (ім'я, прізвище, дата народження)")
    
    if len(password) < 12:
        recommendations.append("Збільште довжину пароля до 12+ символів")
    
    if not re.search(r'[A-Z]', password):
        recommendations.append("Додайте великі літери")
    
    if not re.search(r'[a-z]', password):
        recommendations.append("Додайте малі літери")
    
    if not re.search(r'\d', password):
        recommendations.append("Додайте цифри")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        recommendations.append("Додайте спеціальні символи (!@#$%^&* тощо)")
    
    if strength_score >= 8:
        recommendations.append("Пароль надійний, регулярно змінюйте його")
    
    return recommendations

def main():
    print("=== Аналіз безпеки пароля ===\n")
    
    name, surname, birth_date, password = get_personal_data()
    
    print("\n--- Результати аналізу ---\n")
    
    date_parts = extract_date_components(birth_date)
    personal_issues = check_personal_data_in_password(password, name, surname, date_parts)
    
    if personal_issues:
        print("Виявлені проблеми:")
        for issue in personal_issues:
            print(f"  - Пароль {issue}")
        print()
    else:
        print("Особисті дані не виявлені в паролі\n")
    
    strength_score, criteria = evaluate_password_strength(password)
    
    print(f"Оцінка складності: {strength_score}/10")
    print("Критерії:")
    for criterion in criteria:
        print(f"  - {criterion}")
    print()
    
    recommendations = generate_recommendations(password, personal_issues, strength_score)
    
    if recommendations:
        print("Рекомендації:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("Пароль відповідає базовим вимогам безпеки")
    
    print("\n" + "="*40)

if __name__ == "__main__":
    main()