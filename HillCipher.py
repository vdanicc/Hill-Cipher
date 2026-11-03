def asciiConvert(txt):
    vals = [ord(char) for char in txt]
    while len(vals) % 3 != 0:
        vals.append(0)
    return vals

def matrixTranspose(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in m[:i] + m[i+1:]]

def getMatrixDeterminant(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for c in range(len(m)):
        det += ((-1) ** c) * m[0][c] * getMatrixDeterminant(getMatrixMinor(m, 0, c))
    return det

def getMatrixInverse(m):
    det = getMatrixDeterminant(m) % 256

    if det == 0:
        return "Matrix tidak memiliki invers"

    detInverse = pow(det, -1, 256)
    
    n = len(m)
    if n == 1:
        return [[detInverse % 256]]
    
    cofactors = []
    for r in range(n):
        cofactorRow = []
        for c in range (len(m)):
            minor = getMatrixMinor(m, r, c)
            cofactor = ((-1) ** (r + c)) * getMatrixDeterminant(minor)
            cofactorRow.append(cofactor)
        cofactors.append(cofactorRow)

    adj = matrixTranspose(cofactors)
    inverse = []
    for r in range(n):
        row = []
        for c in range(n):
            row.append((adj[r][c] * detInverse) % 256)
        inverse.append(row)

    return inverse

def matrixMultiply(m, v):
    result = [0, 0, 0]
    for row in range(3):
        total = 0
        for col in range(3):
            total += m[row][col] * v[col]
        result[row] = total % 256
    return result

def encryptText(plaintext, key):
    num = asciiConvert(plaintext)
    ciphertext = []
    for i in range(0, len(num), 3):
        block = num[i:i+3]
        EncryptedBlock = matrixMultiply(key, block)
        ciphertext.extend(EncryptedBlock)
    return ciphertext

def decryptText(ciphertext, inversekey):
    plaintext = []
    for i in range(0, len(ciphertext), 3):
        block = ciphertext[i:i+3]
        DecryptedBlock = matrixMultiply(inversekey, block)
        plaintext.extend(DecryptedBlock)
    return ''.join(chr(num) for num in plaintext if num != 0)

key = [[1, 10, 20],
       [1, 13, 22],
       [1, 10, 25]]

inversekey = getMatrixInverse(key)

name = input("Masukkan nama Anda: ")
print(f"Selamat datang {name}!")
choice = input("Pilih 'enkripsi' atau 'dekripsi': ").strip().lower()

if choice == "enkripsi":
    plaintext = input("Masukkan teks Anda: ")
    ciphertext = encryptText(plaintext, key)
    print(f"Teks yang telah dirahasiakan: {ciphertext}")

elif choice == "dekripsi":
    CipherTextInput = input("Masukkan teks tersandi: ")
    ciphertext = [int(x) for x in CipherTextInput.split(", ")]
    decryptedtext = decryptText(ciphertext, inversekey)
    print(f"Teks yang telah dikembalikan: {decryptedtext}")

else:
    print("Silahkan jalankan program ulang dan pilih 'enkripsi' atau 'dekripsi'.")