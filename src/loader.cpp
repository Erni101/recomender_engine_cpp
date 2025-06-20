#include "loader.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>

namespace recommender {

bool Loader::load_embeddings(const std::string& path, 
                            std::vector<float>& embeddings,
                            std::vector<std::string>& ids) {
    if (!validate_file(path)) {
        return false;
    }
    
    try {
        std::ifstream file(path, std::ios::binary);
        if (!file) {
            return false;
        }
        
        // Read number of items and embedding dimension
        uint32_t num_items, dim;
        file.read(reinterpret_cast<char*>(&num_items), sizeof(num_items));
        file.read(reinterpret_cast<char*>(&dim), sizeof(dim));
        
        // Read IDs
        ids.resize(num_items);
        for (uint32_t i = 0; i < num_items; ++i) {
            uint32_t id_len;
            file.read(reinterpret_cast<char*>(&id_len), sizeof(id_len));
            
            std::vector<char> id_buffer(id_len);
            file.read(id_buffer.data(), id_len);
            ids[i] = std::string(id_buffer.data(), id_len);
        }
        
        // Read embeddings
        size_t total_floats = num_items * dim;
        embeddings.resize(total_floats);
        file.read(reinterpret_cast<char*>(embeddings.data()), 
                 total_floats * sizeof(float));
        
        return file.good();
    } catch (const std::exception& e) {
        std::cerr << "Error loading embeddings: " << e.what() << std::endl;
        return false;
    }
}

bool Loader::load_text_data(const std::string& path, 
                           std::vector<std::string>& data) {
    if (!validate_file(path)) {
        return false;
    }
    
    try {
        std::ifstream file(path);
        if (!file) {
            return false;
        }
        
        std::string line;
        while (std::getline(file, line)) {
            if (!line.empty()) {
                data.push_back(line);
            }
        }
        
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Error loading text data: " << e.what() << std::endl;
        return false;
    }
}

bool Loader::save_embeddings(const std::string& path, 
                           const std::vector<float>& embeddings,
                           const std::vector<std::string>& ids) {
    try {
        std::ofstream file(path, std::ios::binary);
        if (!file) {
            return false;
        }
        
        // Write number of items and embedding dimension
        uint32_t num_items = static_cast<uint32_t>(ids.size());
        uint32_t dim = num_items > 0 ? static_cast<uint32_t>(embeddings.size() / num_items) : 0;
        
        file.write(reinterpret_cast<const char*>(&num_items), sizeof(num_items));
        file.write(reinterpret_cast<const char*>(&dim), sizeof(dim));
        
        // Write IDs
        for (const auto& id : ids) {
            uint32_t id_len = static_cast<uint32_t>(id.size());
            file.write(reinterpret_cast<const char*>(&id_len), sizeof(id_len));
            file.write(id.c_str(), id_len);
        }
        
        // Write embeddings
        file.write(reinterpret_cast<const char*>(embeddings.data()),
                  embeddings.size() * sizeof(float));
        
        return file.good();
    } catch (const std::exception& e) {
        std::cerr << "Error saving embeddings: " << e.what() << std::endl;
        return false;
    }
}

// Private helper methods
bool Loader::validate_file(const std::string& path) {
    std::ifstream file(path);
    return file.good();
}

} // namespace recommender
