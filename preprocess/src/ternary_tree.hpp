#include <cstring>
#include <fstream>
#include <stdexcept>

char  buffer[MAX_STR_SIZE];
//unsigned long long cnt_words;
//std::ofstream file;

typedef int64_t Index;

template <typename T>
class TernaryTreeNode
{
public:
    char c;
    TernaryTreeNode * left;
    TernaryTreeNode * down;
    TernaryTreeNode * right;
    T data;
    Index id;
    TernaryTreeNode():left(NULL),down(NULL),right(NULL),data(0){}
};

class TernaryTree
{
private:

public:
    Index id_global=0;
    TernaryTreeNode<Index> * tree;
    TernaryTree():tree(NULL)
    {
//        tree = new TernaryTreeNode<Index>();
//        tree->c='m';
    }
//Index get_value(const TernaryTreeNode<Index> * node, const char * str) ;
    Index get_id(const char * str);
    Index set_id_and_increment(const char * str);
    TernaryTreeNode<Index> * get_node(const char * str);
    void dump_frequency(const std::string & name_file) const;
    void dump_ids(const std::string & name_file) const;
    void dump_dot(const std::string & name_file) const;
    void reassign_ids();
    size_t count_nodes() const; 
};

Index TernaryTree::set_id_and_increment(const char * str)
{
    if (tree==NULL)
    { 
        //std::cerr<<"creating new head\n";
        tree = new TernaryTreeNode<Index>();
        tree->c=str[0];
    } 
    auto node=tree;
    unsigned int depth=0;
    bool is_done=false;
    if ((strlen(str)==1)&&(node->c==str[0])) is_done=true;
    while (!is_done)
    {
        if (depth>=MAX_STR_SIZE) {std::cerr<<"string too long in tree, aborting \n"; return -1;}
        char c=str[depth];
//        std::cerr<<"depth = "<<depth<<"\tnode.c = "<<node->c<<"\tc = "<<c<<"\n";
        if (c==node->c)
        {
            if (node->down==NULL) 
            {
                node->down= new TernaryTreeNode<Index>();
                node->down->c=str[depth+1];     
//                std::cerr<<"creating down\n";
            }
            node=node->down;
//            std::cerr<<"moving down\n";
            depth++;
            c=str[depth];
           // continue;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)   
            {   
                node->left= new TernaryTreeNode<Index>();
                node->left->c=c;
//                std::cerr<<"creating left\n";
            }
            node=node->left;
//            std::cerr<<"moving left\n";
           // continue;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) 
            {
                node->right= new TernaryTreeNode<Index>();
                node->right->c=c;
            }
            node=node->right;
//            std::cerr<<"moving right\n";
            //continue;
        }
        //if (depth>=strlen(str)) is_done=true;
        if ((depth>=strlen(str)-1)&&(node->c==c)) is_done=true;
    }
    if (!node->data) node->id=id_global++;
    node->data++;
    return node->id;
}

//template <typename T>
/*
Index TernaryTree::get_value(const TernaryTreeNode<Index> * node, const char * str) 
{
    unsigned int depth=0;
    while (depth<strlen(str)-1)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return 0;
            node=node->down;
            depth++;
            continue;
        } 
        if (c<node->c)
        {
            if (node->left==NULL)  return 0;
            node=node->left;
            continue;
        } 
        if (c>node->c)
        {
            if (node->right==NULL) return 0;
            node=node->right;
        }
    }
    return node->data;
}
*/
TernaryTreeNode<Index> * TernaryTree::get_node(const char * str)
{
    auto node=tree;
    unsigned int depth=0;
    //std::cerr<<"fetching id for "<<str<<"\n";
    bool is_done=false;
    while (!is_done)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return NULL;
            node=node->down;
            depth++;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)  return NULL;
            node=node->left;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) return NULL;
            node=node->right;
        }
        c=str[depth];
        //std::cerr<<"depth = "<<depth<<" node.c = "<<node->c<<"\n";
        if ((depth>=strlen(str)-1)&&(node->c==c)) is_done=true;
    }
    return node;
}


Index TernaryTree::get_id(const char * str)
{
    auto node=tree;
    if (node==0) return -1;
    unsigned int depth=0;
    //std::cerr<<"fetching id for "<<str<<"\n";
    bool is_done=false;
    while (!is_done)
    {
        char c=str[depth];
        if (c==node->c)
        {
            if (node->down==NULL) return -1;
            node=node->down;
            depth++;
        } else
        if (c<node->c)
        {
            if (node->left==NULL)  return -1;
            node=node->left;
        } else
        if (c>node->c)
        {
            if (node->right==NULL) return -1;
            node=node->right;
        }
        c=str[depth];
        //std::cerr<<"depth = "<<depth<<" node.c = "<<node->c<<"\n";
        if ((depth>=strlen(str)-1)&&(node->c==c)) is_done=true;
    }
    //std::cerr<<"found at depth "<<depth<<" id = "<<node->id-1<<"\n";
    return node->id;
}

class Action {
public:
    virtual void operator()(TernaryTreeNode<Index>* node,unsigned int depth)=0;
};

class ActionReassignIds: public Action {
public:
    uint64_t current_id;
    ActionReassignIds():current_id(0){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        if (node->data>0) node->id=current_id++;
    }
};

class ActionFile: public Action
{
protected:
    std::ofstream file;
public:
    ActionFile(std::string name_file)
    {
        file.open (name_file);    
        if(!file)  throw  std::runtime_error("can not open output file "+name_file+" , check the path");
    }
    virtual ~ActionFile()
    {
        file.close();
    }
};

class ActionFileWriteFrequency: public ActionFile
{
public:
    ActionFileWriteFrequency(std::string name_file):ActionFile(name_file){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    if (node->data)
        file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->data<<"\n";
    }
};

class ActionFileWriteId: public ActionFile
{
public:
    ActionFileWriteId(std::string name_file):ActionFile(name_file){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    if (node->data)
        file<<std::string(buffer,buffer+depth+1)<<"\t"<<node->id<<"\n";
    }
};

class ActionCountNodes: public Action
{
public:
    size_t cnt;
    ActionCountNodes():cnt(0){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        cnt++;
    }
};

class ActionFileWriteDot: public ActionFile
{
public:
    ActionFileWriteDot(std::string name_file):ActionFile(name_file)
    {
        file<<"digraph tree {\n";
    }
    ~ActionFileWriteDot()
    {
        file<<"}\n";
    }
    
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
    std::string label(buffer,buffer+depth+1);
    file<<label<<" [label="<<node->c<<"];\n";
    if (node->left!=NULL)
    {
        std::string label2=label;
        label2[label2.length()-1]=node->left->c;
        file<<label<<"\t->\t"<<label2<<"  [color=blue];\n";
    }
    if (node->down!=NULL)
    {
        std::string label2=label;
        label2=label2+node->down->c;
        file<<label<<"\t->\t"<<label2<<" [style=dotted];\n";
    }
    if (node->right!=NULL)
    {
        std::string label2=label;
        label2[label2.length()-1]=node->right->c;
        file<<label<<"\t->\t"<<label2<<"[color=red] ;\n";
    }
        
    }
};

void visit_recursively(TernaryTreeNode<Index> * node,unsigned int depth, Action & action)
{
    if (node==NULL) return;
    buffer[depth]=node->c;  
    if (node->left!=NULL) visit_recursively(node->left,depth,action);
    buffer[depth]=node->c;  
    buffer[depth+1]=0;  

    action(node,depth);

    if (node->down!=NULL) visit_recursively(node->down,depth+1,action);
    buffer[depth]=node->c;  
    if (node->right!=NULL) visit_recursively(node->right,depth,action);
    buffer[depth]=node->c;  
}


bool trim(TernaryTreeNode<Index> * * pnode, int64_t threshold, unsigned int depth)
{
    auto node = * pnode;
    if (node==NULL) return true;

    buffer[depth]=node->c;  

    int cnt_kids=3;
    if (trim(&(node->left),threshold,depth))
    {
        cnt_kids--;
    }
    if (trim(&(node->down),threshold,depth+1))
    {
        cnt_kids--;
    }

    if (trim(&(node->right),threshold,depth))
    {
        cnt_kids--;
    }

    if (node->data<threshold)
    {
        if (cnt_kids==0)
        {
            delete *pnode;
            *pnode=NULL;
            return true;
        }
        else
        {
            node->id=-1;
            node->data=0;
        }

    }
    return false;
}

void TernaryTree::dump_frequency(const std::string & name_file) const
{
    ActionFileWriteFrequency a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_dot(const std::string & name_file) const
{
    ActionFileWriteDot a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::dump_ids(const std::string & name_file) const
{
    ActionFileWriteId a(name_file);
    visit_recursively(tree,0,a);
}

void TernaryTree::reassign_ids()
{
    ActionReassignIds a;
    visit_recursively(tree,0,a);
    id_global=a.current_id;
}

size_t TernaryTree::count_nodes() const
{
    ActionCountNodes a;
    visit_recursively(tree,0,a);
    
    return a.cnt;

}
