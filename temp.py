class Person:
    name = 'Adam'


p ={}
print('Before modification:', p.name)

# setting name to 'John'
setattr(p, 'name', 'John')

print('After modification:', p.name)