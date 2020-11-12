import os

search_path = os.path.join('assets/uploads/')

def find_file(filename):
   result = []
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return True if len(result)>0 else False

