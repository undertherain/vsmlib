#include <iostream>
#include <cstring>
#include <fstream>
#include <stdexcept>
#include <vector>

#include "string_tools.hpp"

#if !defined(MAX_STR_SIZE)
#define MAX_STR_SIZE 1000
#endif

typedef int64_t Index;

template <typename T>
class TernaryTreeNode
{
public:
    wchar_t c;
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
    Index get_id(const wchar_t * str);
    Index set_id_and_increment(const wchar_t * str);
    TernaryTreeNode<Index> * get_node(const wchar_t * str);
    void dump_frequency(const std::string & name_file) const;
    void dump_ids(const std::string & name_file) const;
    void dump_dot(const std::string & name_file) const;
    void reassign_ids();
    void reassign_ids_new(std::vector<Index> const  & lst_new_ids);
    void populate_frequency(std::vector<Index> & lst_frequency ) const;
    size_t count_nodes() const; 
};

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

class ActionReassignIdsFreq: public Action {
public:
    std::vector<Index> const & lst_new_ids;
    ActionReassignIdsFreq(std::vector<Index> const & _lst_new_ids):lst_new_ids(_lst_new_ids){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth)
    {
        if (node->data>0) 
            if (node->id>=0) 
        {
           //   std::cerr<<"replaceing "<<node->id<<" with "<<lst_new_ids[node->id]<<"\n";
            node->id=lst_new_ids[node->id];
        }
    }
};

class ActionFile: public Action
{
protected:
    std::ofstream file;
public:
    ActionFile(std::string name_file);
    virtual ~ActionFile();
};

class ActionFileWriteFrequency: public ActionFile
{
public:
    ActionFileWriteFrequency(std::string name_file):ActionFile(name_file){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth);
};

class ActionFileWriteId: public ActionFile
{
public:
    ActionFileWriteId(std::string name_file):ActionFile(name_file){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth);
};

class ActionCountNodes: public Action
{
public:
    size_t cnt;
    ActionCountNodes():cnt(0){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth);
};

class ActionFileWriteDot: public ActionFile
{
public:
    ActionFileWriteDot(std::string name_file);
    ~ActionFileWriteDot();
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth);
};

class ActionPopulateFrequency: public Action
{
public:
    size_t pos;
    std::vector<Index> & lst_frequency;
    ActionPopulateFrequency(std::vector<Index> & _lst_frequency):pos(0), lst_frequency(_lst_frequency){}
    void operator()(TernaryTreeNode<Index>* node,unsigned int depth);
};


void visit_recursively(TernaryTreeNode<Index> * node,unsigned int depth, Action & action);


bool trim(TernaryTreeNode<Index> * * pnode, int64_t threshold, unsigned int depth);