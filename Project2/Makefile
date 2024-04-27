# Compiler and linker configurations
CXX = g++
CXXFLAGS = -g  # Add debug symbols
LDFLAGS =
LDLIBS = -lpthread

# Define the executable file
TARGET = thread_game

# Define source files
SOURCES = thread_game.cpp
OBJECTS = $(SOURCES:.cpp=.o)

# Default rule to build everything
all: $(TARGET)

# Rule to link the program
$(TARGET): $(OBJECTS)
	$(CXX) $(LDFLAGS) $(OBJECTS) -o $@ $(LDLIBS)

# Rule to compile the source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
ifeq ($(OS),Windows_NT)
	del $(TARGET) $(OBJECTS)
else
	rm -f $(TARGET) $(OBJECTS)
endif