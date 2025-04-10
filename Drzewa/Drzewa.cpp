#include <iostream>
#include <vector>
using namespace std;

// Struktura węzła drzewa
struct Node {
    int key;
    Node* left;
    Node* right;
    int height;
    Node(int k) : key(k), left(nullptr), right(nullptr), height(1) {}
};

// Funkcja zwracająca wysokość węzła
int getHeight(Node* n) {
    return n ? n->height : 0;
}

// Funkcja aktualizująca wysokość węzła
void updateHeight(Node* n) {
    if (n) n->height = 1 + max(getHeight(n->left), getHeight(n->right));
}

// Rotacje AVL
Node* rotateRight(Node* y) {
    Node* x = y->left;
    Node* T = x->right;
    x->right = y;
    y->left = T;
    updateHeight(y);
    updateHeight(x);
    return x;
}

Node* rotateLeft(Node* x) {
    Node* y = x->right;
    Node* T = y->left;
    y->left = x;
    x->right = T;
    updateHeight(x);
    updateHeight(y);
    return y;
}

// Balansowanie węzła AVL
Node* balance(Node* n) {
    if (!n) return nullptr;
    updateHeight(n);
    int balanceFactor = getHeight(n->left) - getHeight(n->right);
    if (balanceFactor > 1) {
        if (getHeight(n->left->right) > getHeight(n->left->left))
            n->left = rotateLeft(n->left);
        return rotateRight(n);
    }
    if (balanceFactor < -1) {
        if (getHeight(n->right->left) > getHeight(n->right->right))
            n->right = rotateRight(n->right);
        return rotateLeft(n);
    }
    return n;
}

// Wstawianie do AVL
Node* insertAVL(Node* root, int key) {
    if (!root) return new Node(key);
    if (key < root->key) root->left = insertAVL(root->left, key);
    else root->right = insertAVL(root->right, key);
    return balance(root);
}

// Wstawianie do BST
Node* insertBST(Node* root, int key) {
    if (!root) return new Node(key);
    if (key < root->key) root->left = insertBST(root->left, key);
    else root->right = insertBST(root->right, key);
    return root;
}

// Wyszukiwanie min i max
Node* findMin(Node* root, vector<int>& path) {
    while (root->left) {
        path.push_back(root->key);
        root = root->left;
    }
    path.push_back(root->key);
    return root;
}

Node* findMax(Node* root, vector<int>& path) {
    while (root->right) {
        path.push_back(root->key);
        root = root->right;
    }
    path.push_back(root->key);
    return root;
}

// Usuwanie węzła
Node* remove(Node* root, int key) {
    if (!root) return nullptr;
    if (key < root->key) root->left = remove(root->left, key);
    else if (key > root->key) root->right = remove(root->right, key);
    else {
        if (!root->left) return root->right;
        if (!root->right) return root->left;
        Node* minLargerNode = findMin(root->right, vector<int>());
        root->key = minLargerNode->key;
        root->right = remove(root->right, minLargerNode->key);
    }
    return balance(root);
}

// Traversale
void inOrder(Node* root) {
    if (!root) return;
    inOrder(root->left);
    cout << root->key << " ";
    inOrder(root->right);
}

void preOrder(Node* root) {
    if (!root) return;
    cout << root->key << " ";
    preOrder(root->left);
    preOrder(root->right);
}

void postOrder(Node* root) {
    if (!root) return;
    postOrder(root->left);
    postOrder(root->right);
    cout << root->key << " ";
}

// Usuwanie całego drzewa
Node* deleteTree(Node* root) {
    if (!root) return nullptr;
    root->left = deleteTree(root->left);
    root->right = deleteTree(root->right);
    cout << "Deleting: " << root->key << endl;
    delete root;
    return nullptr;
}

// Pre-order poddrzewa
void preOrderSubtree(Node* root, int key) {
    if (!root) return;
    if (root->key == key) {
        preOrder(root);
        cout << endl;
    } else {
        preOrderSubtree(root->left, key);
        preOrderSubtree(root->right, key);
    }
}

// Równoważenie drzewa BST metodą DSW
Node* createBackbone(Node* root) {
    Node* tmp = root;
    while (tmp) {
        if (tmp->left) {
            tmp = rotateRight(tmp);
        } else {
            tmp = tmp->right;
        }
    }
    return root;
}

Node* balanceTreeDSW(Node* root) {
    root = createBackbone(root);
    return root; // Można dodać dodatkowe operacje rotacji
}

int main() {
    Node* avl = nullptr;
    Node* bst = nullptr;
    vector<int> values = {10, 20, 30, 40, 50, 25};
    for (int v : values) {
        avl = insertAVL(avl, v);
        bst = insertBST(bst, v);
    }

    cout << "Pre-order AVL: "; preOrder(avl); cout << endl;
    cout << "Pre-order BST: "; preOrder(bst); cout << endl;
    
    avl = balanceTreeDSW(avl);
    bst = balanceTreeDSW(bst);
    
    cout << "After balancing AVL: "; preOrder(avl); cout << endl;
    cout << "After balancing BST: "; preOrder(bst); cout << endl;
}
