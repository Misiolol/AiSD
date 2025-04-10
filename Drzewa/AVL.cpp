#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

// Struktura węzła AVL
struct AVLNode {
    AVLNode *up = nullptr, *left = nullptr, *right = nullptr;
    int key = 0;
    int bf = 0; // Balance factor
};

// Łańcuchy do wizualizacji drzewa
string cr, cl, cp;

// =======================
// Funkcja wypisująca drzewo
// =======================
void printTree(string sp, string sn, AVLNode* v) {
    if (v) {
        string s = sp;
        if (sn == cr) s[s.length() - 2] = ' ';
        printTree(s + cp, cr, v->right);

        s = sp.substr(0, sp.length() - 2);
        cout << s << sn << v->key << ":" << v->bf << endl;

        s = sp;
        if (sn == cl) s[s.length() - 2] = ' ';
        printTree(s + cp, cl, v->left);
    }
}

// =======================
// Usuwanie całego drzewa
// =======================
void deleteTree(AVLNode* v) {
    if (v) {
        deleteTree(v->left);
        deleteTree(v->right);
        delete v;
    }
}

// =======================
// ROTACJE
// =======================
void rotateRR(AVLNode*& root, AVLNode* A);
void rotateLL(AVLNode*& root, AVLNode* A);
void rotateRL(AVLNode*& root, AVLNode* A);
void rotateLR(AVLNode*& root, AVLNode* A);

// -----------------------
// Rotacja RR
void rotateRR(AVLNode*& root, AVLNode* A) {
    AVLNode* B = A->right;
    AVLNode* p = A->up;

    A->right = B->left;
    if (A->right) A->right->up = A;

    B->left = A;
    B->up = p;
    A->up = B;

    if (p) {
        if (p->left == A) p->left = B;
        else p->right = B;
    } else root = B;

    if (B->bf == -1) A->bf = B->bf = 0;
    else { A->bf = -1; B->bf = 1; }
}

// -----------------------
// Rotacja LL
void rotateLL(AVLNode*& root, AVLNode* A) {
    AVLNode* B = A->left;
    AVLNode* p = A->up;

    A->left = B->right;
    if (A->left) A->left->up = A;

    B->right = A;
    B->up = p;
    A->up = B;

    if (p) {
        if (p->left == A) p->left = B;
        else p->right = B;
    } else root = B;

    if (B->bf == 1) A->bf = B->bf = 0;
    else { A->bf = 1; B->bf = -1; }
}

// -----------------------
// Rotacja RL
void rotateRL(AVLNode*& root, AVLNode* A) {
    AVLNode* B = A->right;
    AVLNode* C = B->left;
    AVLNode* p = A->up;

    B->left = C->right;
    if (B->left) B->left->up = B;

    A->right = C->left;
    if (A->right) A->right->up = A;

    C->left = A;
    C->right = B;
    A->up = B->up = C;
    C->up = p;

    if (p) {
        if (p->left == A) p->left = C;
        else p->right = C;
    } else root = C;

    A->bf = (C->bf == -1) ? 1 : 0;
    B->bf = (C->bf == 1) ? -1 : 0;
    C->bf = 0;
}

// -----------------------
// Rotacja LR
void rotateLR(AVLNode*& root, AVLNode* A) {
    AVLNode* B = A->left;
    AVLNode* C = B->right;
    AVLNode* p = A->up;

    B->right = C->left;
    if (B->right) B->right->up = B;

    A->left = C->right;
    if (A->left) A->left->up = A;

    C->right = A;
    C->left = B;
    A->up = B->up = C;
    C->up = p;

    if (p) {
        if (p->left == A) p->left = C;
        else p->right = C;
    } else root = C;

    A->bf = (C->bf == 1) ? -1 : 0;
    B->bf = (C->bf == -1) ? 1 : 0;
    C->bf = 0;
}

// =======================
// Wstawianie do drzewa AVL
// =======================
void insertAVL(AVLNode*& root, int key) {
    AVLNode* w = new AVLNode;
    w->key = key;

    if (!root) {
        root = w;
        return;
    }

    AVLNode* p = root;
    while (true) {
        if (key < p->key) {
            if (!p->left) {
                p->left = w;
                break;
            }
            p = p->left;
        } else {
            if (!p->right) {
                p->right = w;
                break;
            }
            p = p->right;
        }
    }

    w->up = p;
    if (p->bf) {
        p->bf = 0;
    } else {
        p->bf = (p->left == w) ? 1 : -1;

        AVLNode* r = p->up;
        bool balanceNeeded = false;

        while (r) {
            if (r->bf) {
                balanceNeeded = true;
                break;
            }
            r->bf = (r->left == p) ? 1 : -1;
            p = r;
            r = r->up;
        }

        if (balanceNeeded) {
            if (r->bf == 1) {
                if (r->right == p) r->bf = 0;
                else if (p->bf == -1) rotateLR(root, r);
                else rotateLL(root, r);
            } else {
                if (r->left == p) r->bf = 0;
                else if (p->bf == 1) rotateRL(root, r);
                else rotateRR(root, r);
            }
        }
    }
}

// =======================
// Usuwanie węzła z drzewa AVL
// =======================
AVLNode* findNode(AVLNode* root, int key) {
    while (root && root->key != key) {
        root = (key < root->key) ? root->left : root->right;
    }
    return root;
}

AVLNode* predecessor(AVLNode* p) {
    AVLNode* r;
    if (p->left) {
        p = p->left;
        while (p->right) p = p->right;
    } else {
        do {
            r = p;
            p = p->up;
        } while (p && p->right != r);
    }
    return p;
}

AVLNode* removeAVL(AVLNode*& root, AVLNode* x) {
    AVLNode *t, *y, *z;
    bool nest;

    if (x->left && x->right) {
        y = removeAVL(root, predecessor(x));
        nest = false;
    } else {
        y = x->left ? x->left : x->right;
        x->bf = 0;
        nest = true;
    }

    if (y) {
        y->up = x->up;
        y->left = x->left; if (y->left) y->left->up = y;
        y->right = x->right; if (y->right) y->right->up = y;
        y->bf = x->bf;
    }

    if (x->up) {
        if (x->up->left == x) x->up->left = y;
        else x->up->right = y;
    } else root = y;

    if (nest) {
        z = y;
        y = x->up;

        while (y) {
            if (!y->bf) {
                y->bf = (y->left == z) ? -1 : 1;
                break;
            }

            if ((y->bf == 1 && y->left == z) || (y->bf == -1 && y->right == z)) {
                y->bf = 0;
                z = y;
                y = y->up;
            } else {
                t = (y->left == z) ? y->right : y->left;

                if (!t->bf) {
                    if (y->bf == 1) rotateLL(root, y);
                    else rotateRR(root, y);
                    break;
                } else if (y->bf == t->bf) {
                    if (y->bf == 1) rotateLL(root, y);
                    else rotateRR(root, y);
                    z = t;
                    y = t->up;
                } else {
                    if (y->bf == 1) rotateLR(root, y);
                    else rotateRL(root, y);
                    z = y->up;
                    y = z->up;
                }
            }
        }
    }

    return x;
}

// =======================
// MAIN
// =======================
int main() {
    AVLNode* root = nullptr;
    int keys[32];

    // Znaki do rysowania drzewa
    cr = cl = cp = "  ";
    cr[0] = 218; cr[1] = 196;
    cl[0] = 192; cl[1] = 196;
    cp[0] = 179;

    srand(time(nullptr));
    for (int i = 0; i < 32; i++) keys[i] = i + 1;

    // Tasujemy klucze
    for (int i = 0; i < 300; i++) {
        int i1 = rand() % 32;
        int i2 = rand() % 32;
        swap(keys[i1], keys[i2]);
    }

    // Wstawiamy do drzewa
    for (int i = 0; i < 32; i++) {
        cout << keys[i] << " ";
        insertAVL(root, keys[i]);
    }

    cout << "\n\nAVL Tree (after insertion):\n";
    printTree("", "", root);

    // Ponowne tasowanie
    for (int i = 0; i < 300; i++) {
        int i1 = rand() % 32;
        int i2 = rand() % 32;
        swap(keys[i1], keys[i2]);
    }

    // Usuwamy 15 węzłów
    cout << "\nDeleting:\n";
    for (int i = 0; i < 15; i++) {
        cout << keys[i] << " ";
        removeAVL(root, findNode(root, keys[i]));
    }

    cout << "\n\nAVL Tree (after deletion):\n";
    printTree("", "", root);

    deleteTree(root);
    return 0;
}
