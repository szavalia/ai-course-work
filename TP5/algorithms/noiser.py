import random

# Adds noise to all elements in font, with probability prob to switch binary value
def noise_font(font, prob):
    new_font = []
    for letter in font:
        new_font.append(noise_elem(letter, prob))
    return new_font


# Adds noise to single character image
def noise_elem(elem, prob):
    new_elem = []
    for bit in elem:
        if random.random() < prob:
            new_elem.append(1 - bit)
        else:
            new_elem.append(bit)
    return new_elem