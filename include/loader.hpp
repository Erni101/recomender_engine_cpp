#pragma once

#include <string>
#include <vector>
#include <fstream>
#include <memory>

namespace recommender {

    class Loader {
    public:
        // Load embeddings from binary file
        static bool load_embeddings(const std::string& path, 
                                   std::vector<float>& embeddings,
                                   std::vector<std::string>& ids);
        
        // Load text data
        static bool load_text_data(const std::string& path, 
                                  std::vector<std::string>& data);
        
        // Save embeddings to binary file
        static bool save_embeddings(const std::string& path, 
                                  const std::vector<float>& embeddings,
                                  const std::vector<std::string>& ids);
        
    private:
        // Helper methods
        static bool validate_file(const std::string& path);
        static bool read_binary_file(const std::string& path, std::vector<float>& data);
        static bool write_binary_file(const std::string& path, const std::vector<float>& data);
    };
}
