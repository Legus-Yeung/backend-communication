"use client"
import { useEffect, useState } from 'react';
import axios from 'axios';
import UserForm from '../app/_components/form';

type User = {
  firstName: string;
  lastName: string;
};

const Home = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get<User[]>('http://127.0.0.1:5000/users');
        setUsers(response.data);
      } catch (error) {
        console.error("Failed to fetch users:", error);
      }
    };
    void fetchUsers();
  }, []);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '20px',
        minHeight: '100vh',
        width: '100%',
        textAlign: 'center'
      }}
    >
      <UserForm />
      <h1>Users</h1>
      <ul>
        {users.map((user, index) => (
          <li key={index}>{user.firstName} {user.lastName}</li>
        ))}
      </ul>
    </div>
  );
};

export default Home;
