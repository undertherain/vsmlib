void trim3(std::string & str)
{
  str.erase(str.begin(), find_if(str.begin(), str.end(), [](char& ch)->bool { return !isspace(ch); }));
  str.erase(find_if(str.rbegin(), str.rend(), [](char& ch)->bool { return !isspace(ch); }).base(), str.end());
  for (unsigned int i=0;i<str.length();i++)
  {
  	if (!isalpha(str[i])) str[i]='_';
  }
   //return str;
}  

void trim_c(char ** str)
{
	
}

